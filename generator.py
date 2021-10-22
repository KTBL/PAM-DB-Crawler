import os

TYPE_MAP = {
    'VARCHAR2': 'TEXT',
    'NUMBER': 'NUMERIC',
    'CHAR': 'TEXT'
}


def extract_fields(definition):
    fields = dict()
    all_fields = definition.split('\n')
    for i, field in enumerate(all_fields):
        field = field.strip()
        f_name, f_type = field.split()
        f_name = f_name.lower()
        effective_type = TYPE_MAP[f_type]
        fields[f_name] = effective_type

    return fields


def create_table_stmt(name, fields):
    stmt = f'CREATE TABLE {name.lower()}('
    for i, field in enumerate(fields.items()):
        f_name, f_type = field
        stmt += f'{f_name.lower()} {f_type}'
        if not i == (len(fields) - 1):
            stmt += ', '
    stmt += ')'
    return stmt


def create_insert_stmt(name, fields):
    columns = f''
    values = f''
    values_prep = f''
    for i, field in enumerate(fields.items()):
        f_name, _ = field
        columns += f'{f_name}'
        values_prep += '?'
        values += f"data['{f_name.lower()}']"
        if not i == (len(fields) - 1):
            columns += ', '
            values += ', '
            values_prep += ', '
    stmt = f'INSERT INTO {name.lower()}({columns}) values({values_prep})'
    return stmt, values


def create_model(name, definition, endpoint, out_dir):
    out_path = os.path.join(out_dir, name.lower() + '.py')
    fields = extract_fields(definition)
    header = """
# DO NOT CHANGE MANUALLY! THIS FILE WAS GENERATED!
import requests


"""
    clazz = f"class {name.capitalize()}:"
    init = f"""
    def __init__(self):
        self.endpoint = '{endpoint}'
    """
    create_table = f"""
    def create_table(self, db_con):
        cursor = db_con.cursor()
        cursor.execute('''{create_table_stmt(name, fields)}''')
        db_con.commit()
            """
    insert_stmt, values = create_insert_stmt(name, fields)
    store_row = f"""
    def store(self, data, db_con):
        cursor = db_con.cursor()
        cursor.execute('''{insert_stmt}''', ({values}))
        db_con.commit()
            """
    pull = f"""
    def pull(self, db_con, offset):
        resp = requests.get(self.endpoint + str(offset))
        data = resp.json()
        for row in data['items']:
            self.store(row, db_con)
        return data['hasMore'], data['offset'] + data['count']
    """
    with open(out_path, 'w') as file:
        file.writelines([header, clazz, init, create_table, store_row, pull])
    return name.capitalize(), name.lower()

