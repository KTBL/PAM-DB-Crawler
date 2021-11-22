import os


TYPE_MAP = {
    'VARCHAR2': 'TEXT',
    'NUMBER': 'NUMERIC',
    'CHAR': 'TEXT',
    'DATE': 'TIMESTAMP'
}


def extract_fields(definition):
    # Field / Column information is extracted from the definition
    # provided. The field / column type provided cannot be used directly.
    # Therefore, we use the TYPE_MAP mapping provided above.
    # Whitespaces within a line are stripped away.
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
    # The create table statement s simple:
    # CREATE TABLE foo(baz, bar, boo)
    # We simply take the information of the fields and for each field
    # we create a column.
    stmt = f'CREATE TABLE IF NOT EXISTS {name.lower()}('
    for i, field in enumerate(fields.items()):
        f_name, f_type = field
        stmt += f'{f_name.lower()} {f_type}'
        if not i == (len(fields) - 1):
            stmt += ', '
    stmt += ')'
    return stmt


def create_insert_stmt(name, fields):
    # The Insert statement is a prepared statement. This function returns
    # this prepared statement, but also the list of parameters to fill the
    # prepped statement.
    # Format: INSERT INTO Foo(bar, baz, boo) VALUES (?, ?, ?)
    # Note: yes, the code below can be simplified and prettified
    # But, even though this code is verbose, I think this is easier
    # to understand, and, in something needs to be changed, this can be
    # done very punctual.
    columns = f''  # List of columns
    values = f''  # List of values, must in the order of list of columns!
    values_prep = f''  # List of preparation symbols ('?')
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
    """
    This is the main function of the generator.

    Important: This function uses multiline-strings. Multiline-strings are whitespace
    aware. Since python requires strict whitespacing and indentation we make use of
    the whitespace-awareness.

    :param name: Name of the Model and thus also the table.
    :param definition: Definition of the Model as provided in definitions.definition.
    :param endpoint: Endpoint information as provided in definitions.endpoint
    :param out_dir: Path where to save the generated model. Filename is the passed name in lower-case
    :return: Name of the Model-class and name of the file / module generated.
    """
    out_path = os.path.join(out_dir, name.lower() + '.py')
    # First, we extract the fields from the model-definition.
    fields = extract_fields(definition)
    # The Header gives a short notice, that this model is generated. Manual changes
    # are therefore not the best option in case this file is generated again.
    # Furthermore: Any imports needed by this model (oder this module) have to
    # be placed in here.
    # Since this stuff must be un-indented, we use this strange looking format
    # for the string.
    header = """
# DO NOT CHANGE MANUALLY! THIS FILE WAS GENERATED!
import requests


"""

    # The class-definition must be un-indented as well, but for the ease of readability
    # we use a single-line string here
    clazz = f"class {name.capitalize()}:"
    # Here, the fun starts.
    # Everything below must be indented, since it is part of the class we have defined
    # just before and thus, we indent the strings.
    # The endpoint is already given, and we want to 'hardcode' it. So, we have to set
    # it in the init method.
    init = f"""
    def __init__(self):
        self.endpoint = '{endpoint}'
    """

    # Creation of the database-table is done via a method (ok.. it could be a static
    # method as well, but .. yeah.. )
    # To simplify this generator function, the Create Table Statement itself is
    # created using the create_table_stmt(...) function.
    create_table = f"""
    def create_table(self, db_con):
        cursor = db_con.cursor()
        cursor.execute('''{create_table_stmt(name, fields)}''')
        db_con.commit()
            """

    # Next up, we create a method to insert a new row into the database. Again, to
    # simplify this generator function, the statement itself is generated in another
    # function.
    insert_stmt, values = create_insert_stmt(name, fields)
    store_row = f"""
    def store(self, data, db_con):
        cursor = db_con.cursor()
        cursor.execute('''{insert_stmt}''', ({values}))
        db_con.commit()
            """

    # The (currently) last method we need is the pull-method. This one is used to
    # pull data from the endpoint we have hardcoded in the init-method.
    # It takes an offset as parameter used by the API.
    # Any data received during the request is stored to the database.
    # Currently NO (!!!!) error handling is provided in here. We keep it simple,
    # stupid and assume this is a simple, stupid API where not much can go wrong
    # and thus we do not have to handle anything in here.
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

