from django import template

from . import noteBar as nb

register = template.Library()  # Djangoのテンプレートタグライブラリ

# カスタムフィルタとして登録する


@register.filter
def color(pk):
    if pk.startswith('H4'):
        return 'is-dark'
    elif pk.startswith('H3'):
        return 'is-danger '
    elif pk.startswith('H2'):
        return 'is-danger is-light'
    elif pk.startswith('H1'):
        return 'is-warning is-light'
    elif pk.startswith('M2'):
        return 'is-success is-light'
    elif pk.startswith('M1'):
        return 'is-info is-light'
    elif pk.startswith('L1'):
        return 'is-link is-light'
    elif pk.startswith('L2'):
        return 'is-link'
    elif pk.startswith('L3'):
        return 'is-link is-dark'
    elif pk.startswith('L4'):
        return 'is-link is-black'
    else:
        return 'is-light'


@register.filter
def key_up_down(diff):
    if diff < -6 and diff > -12:
        return '＋'+str(diff+12)+' (オク下)'
    elif diff == -6:
        return '±0 (オク下)'
    elif diff > -6 and diff < 0:
        return '－' + str(abs(diff))
    elif diff == 0:
        return '±0'
    else:
        return diff
