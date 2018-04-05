class RepresentationMixin(object):
    def to_react_representation(self, context=None):
        raise NotImplementedError(
            'Missing property to_react_representation in class'
        )
