import importlib
import json
import logging
import os.path
import sqlite3
import time

from definitions import definition, endpoints
from generator import create_model

state_file_path = './.psm_db_crawler.state.json'
logging.basicConfig(level=logging.DEBUG)


def main():
    # Holding the name mapped to the according class objects.
    # Basically this is not needed after we have created
    # our instances, but is it useful in case one wants to
    # peek into the stuff generated using a debugger or
    # code. Sooo, we leave it in here.
    clazzes = dict()
    # Holding the name mapped to exactly on instance of the
    # model class.
    instances = dict()
    # Holding state information mapped to the name.
    # The information is whether the API has more data to
    # provide and the current offset to use next.
    state = dict()

    # Currently we simply use a sqlite connection.
    # If the generator is change, here could be basically
    # any database be used.
    db_con = sqlite3.connect('./pam-db')

    logging.info("Initializing..")
    init(db_con, state, instances, clazzes)
    logging.info("..done")
    logging.info("Time to crawl!")
    crawl(db_con, state, instances)


def load_state():
    pass


def save_state(state):
    logging.info(f'Storing state at {state_file_path}..')
    with open(state_file_path, 'w') as fp:
        json.dump(state, fp)
    logging.info('..done')


def init(db_con, state, instances, clazzes):
    # Initially we  generate our models, and load the dynamically
    for name, model in definition.items():
        class_name, module_name = create_model(name, model, endpoints[name], './models')
        # Importing the module we have just created
        module = importlib.import_module(f"models.{module_name}")
        # Even though we have the module, we have
        # have to fetch the class object
        clazz = getattr(module, class_name)
        clazzes[class_name] = clazz
        # and instantiate it.
        instance = clazz()
        instance.create_table(db_con)
        instances[class_name] = instance
        # Our initial state starts at "has more"
        # and offset 0 (well, its obvious, isn't it?)
        state[class_name] = {
            'has_more': True,
            'offset': 0,
        }
    if os.path.isfile(state_file_path):
        logging.info(f"Found a state file at {state_file_path}")
        with open(state_file_path, 'r') as fp:
            saved_state = json.load(fp)
            # We fill in the saved state endpoint by endpoint
            # to prevent overwriting any endpoints' state
            # we have yet not in the latest save file.
            # Something like this could happen, if the definitions
            # are extended and one does not want to dismiss the
            # current state of the DB
            for name, state_info in saved_state.items():
                logging.info(f"Loading saved state for {name}")
                # Here we set the has_more parameter to true,
                # so the crawler will check, whether there are
                # still no more elements to crawl.
                state_info['has_more'] = True
                state[name] = state_info


def crawl(db_con, state, instances):
    # Next we start downloading stuff.
    # This is done endpoint (aka model) by model.
    # If one is finished, we start the next one. This means,
    # we are not downloading stuff in parallel!
    # Since we do not want to stress the endpoint-server
    # too much, we use a delay of 10 seconds in between each
    # query.
    retries = 0
    max_retries = 3
    for name, api in instances.items():
        api_state = state[name]

        while api_state['has_more']:
            # Those two are defined right here,
            # so we can access them below in
            # when handling a KeyboardInterrupt.
            #
            # Also they are reset every loop.
            # This is needed, because we don't
            # want to mess up / mix up has_more
            # and offset information of different
            # api_states in case an interrupt appears
            # right before the pull call.
            has_more = None
            next_offset = None
            try:
                logging.info(f"pull {name}..")
                try:
                    has_more, next_offset = api.pull(db_con, api_state['offset'])
                except IOError as e:
                    retries += 1
                    logging.error(f"An IOError occurred while pulling. Try {retries} of {max_retries}",
                                  exc_info=e,
                                  stack_info=True)
                    if retries > max_retries:
                        logging.warning("Max retries reached, stopping the crawl.")
                        return
                    # else
                    continue
                if retries > 0:
                    retries = 0
                api_state['has_more'] = has_more
                api_state['offset'] = next_offset
                logging.info(f"has_more={has_more}, next_offset={next_offset}")
                time.sleep(10)
                # uncomment the following line to do a test run with only a single pull per endpoint
                #        api_state['has_more'] = False
            except KeyboardInterrupt:
                logging.warning("Caught a KeyboardInterrupt.")
                logging.info("Saving the current state..")
                if has_more and next_offset:
                    api_state['has_more'] = has_more
                    api_state['offset'] = next_offset
                save_state(state)
                logging.info(".. done")
                logging.info("Time to say goodbye..")
                return
        logging.info(f"{name} doesn't have any more items")


if __name__ == '__main__':
    main()


