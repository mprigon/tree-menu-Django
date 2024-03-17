from django.db import connection


def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def menu_all(path):
    with connection.cursor() as cursor:
        cursor.execute(
            "WITH RECURSIVE tree(id, name, parent_id, path, depth, item_index, item_name) \
            AS(SELECT id, name, parent_id, id, 1, 1, name \
                FROM tree_item WHERE tree_item.parent_id IS NULL \
                UNION ALL \
                SELECT ti.id, ti.name, ti.parent_id, \
                        path || '/' || ti.id, depth + 1, \
                        item_index || '.' || ti.id, item_name || '/' || ti.name \
                FROM tree_item ti \
                INNER JOIN tree t \
                ON ti.parent_id = t.id \
               ) \
            SELECT * FROM tree \
            ORDER BY item_name")

        sql_raw_result = dictfetchall(cursor)
        """ Returns list of dictionaries with column names """

    print('path: ', path, type(path))
    path_str = str(path)
    print('path_str: ', path_str)
    print('sql_raw_result: ', sql_raw_result)

    # ищем словарь в списке словарей, соответствующий path из url
    # чтобы потом передать в template подробности о выбранном пункте меню
    i = 0
    id_result = False
    while i < len(sql_raw_result):
        id_str = str(sql_raw_result[i]["path"])
        print('id_str: ', id_str)
        if id_str == path_str:
            id_result = True
            i_details = i
            break
        i += 1
        continue

    if id_result:
        print('словарь с path соответствующим url найден: ', sql_raw_result[i_details])
    else:
        print('path не найден в списке путей меню')

    assert sql_raw_result[0]["parent_id"] is None, "First element in sql_raw_result should be root"
    sql_raw_result[0]["root"] = True
    sql_raw_result[0]["in"] = False
    sql_raw_result[0]["out"] = False
    sql_raw_result[0]["same_level"] = False
    i = 1
    while i < len(sql_raw_result):
        sql_raw_result[i]["root"] = False
        delta_depth = sql_raw_result[i]["depth"] - sql_raw_result[i-1]["depth"]
        sql_raw_result[i]["delta_depth"] = delta_depth
        if delta_depth > 0:
            sql_raw_result[i]["in"] = True
            sql_raw_result[i]["out"] = False
            sql_raw_result[i]["same_level"] = False
            i += 1
            continue
        elif delta_depth < 0:
            sql_raw_result[i]["out"] = True
            sql_raw_result[i]["out_list"] = ["out"] * abs(delta_depth)
            # out_list используется, чтобы несколько раз ввести тег </ul>
            sql_raw_result[i]["in"] = False
            sql_raw_result[i]["same_level"] = False
            i += 1
            continue
        else:
            sql_raw_result[i]["same_level"] = True
            sql_raw_result[i]["in"] = False
            sql_raw_result[i]["out"] = False
            i += 1
            continue

    # последний словарь в списке должен закрыть все открытые <ul>
    i_last = len(sql_raw_result) - 1
    sql_raw_result[i_last]["out"] = True
    sql_raw_result[i_last]["out_list"] = ["out"] * sql_raw_result[i_last]["depth"]

    print('modified_sql_raw_result: ', sql_raw_result)

    if id_result:
        context = {"path": path, "id_result": id_result, "sql_details": sql_raw_result[i_details],
                   "sql_raw_result": sql_raw_result}
    else:
        context = {"path": path, "id_result": id_result, "sql_raw_result": sql_raw_result}

    return context
