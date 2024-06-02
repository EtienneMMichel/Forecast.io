import dash
import json


def set_pages(_pages):
    to_save = []
    for page in _pages:
        page.pop('layout', None)
        to_save.append(page)
    with open('pages.json', 'w', encoding='utf-8') as f:
        json.dump(to_save, f, ensure_ascii=False, indent=4)


def get_pages():
    with open('pages.json', encoding='utf-8') as fh:
        pages = json.load(fh)
    return pages

def get_analytics_pages(page):
    path = page["module"].split(".")
    if len(path) > 2 and path[1] == "analytics":
        return True
    return False
