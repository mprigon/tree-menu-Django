from django.shortcuts import render

from.menu import menu_all


def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def index(request):
    path = '/'
    context = menu_all(path)

    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM tree_item")
    #     sql_raw_result = dictfetchall(cursor)
    #     """ Returns list of dictionaries with column names """
    #     # sql_raw_result = cursor.fetchall()
    #     """ Returns list of tuples without column names """

    print('context: ', context)

    return render(request, "tree/index.html", context)


def details(request, path):
    context = menu_all(path)
    return render(request, "tree/item_details.html", context)
