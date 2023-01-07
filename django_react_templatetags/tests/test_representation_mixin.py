from django.test import SimpleTestCase

from django_react_templatetags.mixins import RepresentationMixin


class RepresentationMixinTest(SimpleTestCase):
    def test_implementation_error_raised_if_not_fully_implemented(self):
        class MyObj(RepresentationMixin, object):
            pass

        instance = MyObj()

        with self.assertRaises(NotImplementedError) as err:
            instance.to_react_representation()

        self.assertEquals(
            str(err.exception), "Missing property to_react_representation in class"
        )
