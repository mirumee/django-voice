from djangovoice.models import Type
from django.template import Library,Node

register = Library()

def build_type_list(parser, token):
    """
    {% get_type_list %}
    """
    return TypeObject()

class TypeObject(Node):
    def render(self, context):
        context['type_list'] = Type.objects.all()
        return ''

register.tag('get_type_list', build_type_list)
