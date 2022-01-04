from django.core.serializers.json import DjangoJSONEncoder

from django_react_templatetags.mixins import RepresentationMixin


def json_encoder_cls_factory(context):
    class ReqReactRepresentationJSONEncoder(ReactRepresentationJSONEncoder):
        context = None

    ReqReactRepresentationJSONEncoder.context = context
    return ReqReactRepresentationJSONEncoder


class ReactRepresentationJSONEncoder(DjangoJSONEncoder):
    """
    Custom json encoder that adds support for RepresentationMixin
    """

    def default(self, o):
        if isinstance(o, RepresentationMixin):
            args = [self.context if hasattr(self, "context") else None]
            args = [x for x in args if x is not None]

            return o.to_react_representation(*args)

        return super(ReactRepresentationJSONEncoder, self).default(o)
