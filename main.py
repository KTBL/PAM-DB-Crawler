import importlib
import sqlite3
import time

from definitions import definition, endpoints
from generator import create_model


clazzes = dict()
instances = dict()
state = dict()

db_con = sqlite3.connect('./pam-db')

for name, model in definition.items():
    class_name, module_name = create_model(name, model, endpoints[name], './models')
    module = importlib.import_module(f"models.{module_name}")
    clazz = getattr(module, class_name)
    clazzes[class_name] = clazz
    instance = clazz()
    instance.create_table(db_con)
    instances[class_name] = instance
    state[class_name] = {
        'has_more': True,
        'offset': 0,
    }


for name, api in instances.items():
    api_state = state[name]
    while api_state['has_more']:
        print(f"pull {name}..")
        has_more, next_offset = api.pull(db_con, api_state['offset'])
        api_state['has_more'] = has_more
        api_state['offset'] = next_offset
        print(f"hasmore={has_more}, next_offset={next_offset}")
        time.sleep(5)
    print(f"{name} doesn't have any more items")
print()


