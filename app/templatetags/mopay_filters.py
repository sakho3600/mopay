from django import template

register = template.Library()

@register.filter
def is_selected(value, page_name):
    """custom django filter to check and apply extra style if currently viewed
     page is selected from navigation
     
     Usage:
     {{ "link_on_navigation_name"|is_selected:current_page_name }}.
     """
    s = ''
    if page_name == value:
        s = "class='selected'"
    return s

@register.filter
def mod(value):
    """ simple modulus 2 custom tag. """
    if value % 2 == 0:
        return True
    else:
        return False
    
@register.filter 
def get(value, key):
    """ Get the value of a key from a dict """
    try:
        return value[key]
    except KeyError:
        return None

@register.filter
def from_html(value):
    """
    replaces <p></p> with a new line for display in textbox
    """
    try:
        return value.replace('<br />', '\n')
    except Exception:
        return ''

@register.filter
def to_friendly_url(value):
    """
    Converts string to a url friendly string.
    Replaces all spaces with hyphen and & xter with and
    """
    _value = value.replace(" ", '-')
    _value = _value.replace('&', 'and')
    return _value