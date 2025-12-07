
def parse_sql(sql_file):
    with open(sql_file, "r" ) as sql:
        output = '@startuml'
        tables = {}
        final_dict = {}
        in_table = False
        relationships = set()
        keywords = {' INT': 'Integer', 'VARCHAR': 'String', 'TEXT': 'String', 'DECIMAL': 'Float'}
        relationships = []
        for line in sql.readlines():
            curr_kw = ''
            line = line.strip()
            if line and not line.startswith('--'):
                if line.startswith('CREATE TABLE'):
                    table_name = line[13:-2]
                    tables[table_name] = {}
                    in_table = True

                elif line == ");":
                    in_table = False
                elif in_table:
                    for kw in keywords.keys():
                        if kw in line:
                            curr_kw = kw
                            break
                    if curr_kw:
                        index = line.index(curr_kw)
                        value = line[:index].strip()
                        if f'{table_name[:-1]}_id' == value:
                            pass ## This checks to make sure a tables own ID doesn't get added here (sql2)
                        elif value != 'id':
                            tables[table_name][value] = keywords[curr_kw]
        for table in tables:
            final_dict[table] = {}
            for value in tables[table]:

                if 'id' in value:
                    curr_idx = value.index('id')
                    new_value = value[:curr_idx-1]
                    if (new_value, table) not in relationships:
                        relationships.append((table, new_value))
                    final_dict[table][new_value] = new_value
                else:
                    final_dict[table][value] = tables[table][value]

        first_table = True
        for table in final_dict:
            if first_table:
                output += f'\n    class {table[0].upper()}{table[1:]}' + ' {'
                first_table = False
            else:
                output += '\n    }' + f'\n    class {table[0].upper()}{table[1:]}' + ' {'
            for value in final_dict[table]:
                output += f'\n       +{final_dict[table][value][0].upper()}{final_dict[table][value][1:]} {value}'
        if not first_table:
            output += '\n    }'
        
        for start, end in relationships:
            output += f'\n    {start[0].upper()}{start[1:]} -- {end[0].upper()}{end[1:]}'
        output += '\n@enduml'

        with open('plantuml_export.txt', "w") as f:
            f.write(output)

        return output

def print_uml_from_schema(schema_file):
    print(parse_sql(schema_file))