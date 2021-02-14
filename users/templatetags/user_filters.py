from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def addtag(request, tag):
    updated_request = request.GET.copy()
    if updated_request.get(tag):
        updated_request.pop(tag)
    else:
        updated_request[tag] = False
    return updated_request.urlencode()


@register.filter
def tagtopaginator(page, request):
    updated_request = request.GET.copy()
    updated_request['page'] = page
    return updated_request.urlencode()
