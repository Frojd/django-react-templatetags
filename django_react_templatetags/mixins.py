class RepresentationMixin(object):
    @property
    def react_representation(self):
        raise NotImplementedError(
            'Missing property react_representation in class'
        )
