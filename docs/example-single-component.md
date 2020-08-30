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

    <script id="Menu_dc998396f44d4f178f83486a3c61bce9_data" type="application/json">{"example": 1}</script>
    <script>
        ReactDOM.render(
            React.createElement(
                Menu,
                JSON.parse(document.getElementById("Menu_dc998396f44d4f178f83486a3c61bce9_data").textContent)
            ),
            document.getElementById('Menu_dc998396f44d4f178f83486a3c61bce9')
        );
    </script>

</html>
```

