# Working with models

In this example, by adding `RepresentationMixin` as a mixin to the model, the templatetag will know how to generate the component data. You only need to pass the model instance to the `react_render` templatetag.

This model...

```python
from django.db import models
from django_react_templatetags.mixins import RepresentationMixin

class Person(RepresentationMixin, models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def to_react_representation(self, context={}):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
        }
```

...and this view

```python
import myapp.models import Person

def person_view(request, pk):
    return render(request, 'myapp/index.html', {
        'menu_data': {
            'person': Person.objects.get(pk=pk),
        },
    })
```

...and this template:

```html
{% load react %}
<html>
    <head>...</head>

    <body>
        <nav>
            {% react_render component="Menu" props=menu_data %}
        </nav>
    </body>

    {% react_print %}
</html>
```

...will transform into this:

```html
...

<script>
    ReactDOM.render(
        React.createElement(Menu, {"first_name": "Tom", "last_name": "Waits"}),
        document.getElementById('Menu_405190d92bbc4d00b9e3376522982728')
    );
</script>
```

