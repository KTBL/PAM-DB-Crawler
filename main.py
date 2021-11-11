import importlib
import sqlite3
import time

from definitions import definition, endpoints
from generator import create_model


# Ok ok ok.
# By now, this is a straight forward, single run,
# start and leave it alone script.
# Currently no state-management is provided. This
# code runs from top to bottom, nothing more,
# nothing less.

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


# Next we start downloading stuff.
# This is done endpoint (aka model) by model.
# If one is finished, we start the next one. This means,
# we are not downloading stuff in parallel!
# Since we do not want to stress the endpoint-server
# too much, we use a delay of 10 seconds in between each
# query.
for name, api in instances.items():
    api_state = state[name]
    while api_state['has_more']:
        print(f"pull {name}..")
        has_more, next_offset = api.pull(db_con, api_state['offset'])
        api_state['has_more'] = has_more
        api_state['offset'] = next_offset
        print(f"hasmore={has_more}, next_offset={next_offset}")
        time.sleep(10)
# uncomment the following line to do a test run with only a single pull per endpoint
#        api_state['has_more'] = False
    print(f"{name} doesn't have any more items")
print()


