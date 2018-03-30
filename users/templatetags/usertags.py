from django import template


register = template.Library()


@register.inclusion_tag('users/inc/usertag.html')
def usertag(user):
    return {
        'user': user,
    }
