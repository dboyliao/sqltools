import sqlparse

def table_info(conn, table_name, show = True):
    """
    Show table information according to table_name

    Input:
        conn: a connection object to the database.
        table_nam (string): a string of the table_name.
    
    Return: None
    """
    sql_cmd = "PRAGMA table_info({table_name})"
    cursor = conn.cursor()
    cursor.execute(sql_cmd.format(table_name = table_name))
    _table_info = cursor.fetchall()
    try:
        _cols_len = list(map(lambda d: len(d[1]), _table_info))
        _max_col_len = max(_cols_len)
        sep_line = "+{0:-<"+ str(_max_col_len + 2) + "}+"+ 14*"-" + "+" + "-"*10 + "+" + "-"*10 + "+" + "-"*9 + "+" + "-"*7 + "+"
        if show:
            print(sep_line.format(''))
        row_format = "|{0:<" + str(_max_col_len + 2) + "}|" + "{1:<14}" + "|" + "{2:<10}" + "|" + "{3:<10}" + "|" + "{4:<9}" + "|" + "{5:<7}|"
        if show:
            print(row_format.format("Column", "Type", "Not NULL", "Column No.", "Default", "Primal"))
            print(sep_line.format(''))
        all_cols = []
        for _ in _table_info:
            _ = tuple(map(str, _))
            if show:
                print(row_format.format(_[1], _[2], _[3], _[0], _[4], _[5]))
            all_cols.append(_[1])
        if show:
            print(sep_line.format(''))
        return 0, all_cols
    except ValueError as e:
        print("No such table in the database: ", e)
        return 1, None
    
def _parse_columns(query):
    q = sqlparse.format(query, keyword_case = "upper")
    select_q, table_name, *_ = q.split("FROM")
    temp = select_q.split(" ")
    return [name.strip(",") for name in temp if name not in ['SELECT', '']], table_name.strip()

def show(conn, query):
    colnames, table_name = _parse_columns(query)
    if len(colnames) == 1 and colnames[0] == '*':
        status, colnames = table_info(conn, table_name, False)
    col_len = list(map(lambda n: len(n), colnames))
    sep = '+'
    for l in col_len:
        sep += "-" * (l + 8) + '+'
    print(sep)
    header = "|"
    for ind in range(len(colnames)):
        header += "{" + str(ind) + ":<{0}".format(col_len[ind]+8) + "}|"
    print(header.format(*colnames))
    print(sep)
    c = conn.cursor()
    c.execute(query)
    data = c.fetchall()
    for d in data:
        d = tuple(map(lambda x: str(x), d))
        print(header.format(*d))
    print(sep)