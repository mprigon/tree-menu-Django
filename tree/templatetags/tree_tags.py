from django import template

from tree.models import Item


register = template.Library()


@register.simple_tag()
def get_items():
    return Item.objects.all()


@register.inclusion_tag('tree/include.html')
def draw_menu(menu_all):
    menu_result = menu_all
    return {"menu_result": menu_result}
