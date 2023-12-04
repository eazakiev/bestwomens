from women.utils import menu


def get_women_context(request):
    """Получение контекста для меню"""
    return {"mainmenu": menu}
