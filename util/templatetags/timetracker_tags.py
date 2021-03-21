from django import template
from django.conf import settings
from django.contrib.auth.models import User

from wagtail.core.models import Page, PageViewRestriction, Site
from wagtail.search.models import Query

register = template.Library()

@register.simple_tag(takes_context=True)
def get_site_root(context):
    # NB this returns a core.Page, not the implementation-specific model used
    # so object-comparison to self will return false as objects would differ
    return Site.find_for_request(context['request']).root_page

@register.simple_tag(takes_context=True)
def get_site(context):
    # NB this returns a core.Page, not the implementation-specific model used
    # so object-comparison to self will return false as objects would differ
    return Site.find_for_request(context['request']).site_name

@register.simple_tag(takes_context=True)
def check_page_view_restrictions(context, page):
    """
    Check whether there are any view restrictions on this page which are
    not fulfilled by the given request user.
    """
    request = context['request']
    user = request.user
    for restriction in page.get_view_restrictions():
        if restriction.restriction_type == PageViewRestriction.GROUPS:            
            if not request.user.is_superuser:
                current_user_groups = request.user.groups.all()
            else: 
                return True
            if not any(group in current_user_groups for group in restriction.groups.all()):
                return False
    return True

# Retrieves the top menu items - the immediate children of the parent page
@register.inclusion_tag('util/tags/top_menu.html', takes_context=True)
def top_menu(context, parent, calling_page=None):
    request = context['request']
    if request.user.is_authenticated:
        menuitems = parent.get_children().live().in_menu()
    else:
        menuitems = parent.get_children().live().in_menu().public()
    for menuitem in menuitems:
        # We don't directly check if calling_page is None since the template
        # engine can pass an empty string to calling_page
        # if the variable passed as calling_page does not exist.
        
        menuitem.active = (calling_page.url.startswith(menuitem.url)
                           if calling_page else False)
    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }
