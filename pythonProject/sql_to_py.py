
def parse_sql(sql_file):
    with open(sql_file, "r" ) as sql:
        tables = {}
        in_table = False
        keywords = {' INT', 'VARCHAR', 'TEXT', 'DECIMAL'}
        for line in sql.readlines():
            curr_kw = ''
            line = line.strip()
            if line and not line.startswith('--'):
                print(line)
                if line.startswith('CREATE TABLE'):
                    table_name = line[13:-2]
                    tables[table_name] = []
                    in_table = True

                elif line == ");":
                    in_table = False
                elif in_table:
                    for kw in keywords:
                        if kw in line:
                            curr_kw = kw
                            break
                    if curr_kw:
                        index = line.index(curr_kw)
                        value = line[:index].strip()
                        tables[table_name].append(value)



        print(tables)


parse_sql("schema.txt")