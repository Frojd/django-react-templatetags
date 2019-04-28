# Single Component Example

This view...

```python
from django.shortcuts import render

def menu_view(request):
    return render(request, 'myapp/index.html', {
        'menu_data': {
            'example': 1,
        },
    })
```

... and this template:

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

Will transform into this:

```html
<html>
    <head>...</head>

    <body>
        <nav>
            <div id="Menu_405190d92bbc4d00b9e3376522982728"></div>
        </nav>
    </body>

    <script>
        ReactDOM.render(
            React.createElement(Menu, {"example": 1}),
            document.getElementById('Menu_405190d92bbc4d00b9e3376522982728')
        );
    </script>
</html>
```

