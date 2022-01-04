# Getting started

### Requirements

- Python 3.7+
- Django 3.2+


### Installation

Install the library with pip:

```
$ pip install django_react_templatetags
```


### Adding to django

Make sure `django_react_templatetags` is added to your `INSTALLED_APPS`.

```python
INSTALLED_APPS = (
    # ...
    'django_react_templatetags',
)
```

You also need to add the `react_context_processor` into the `context_middleware`:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates...',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                ...
                'django_react_templatetags.context_processors.react_context_processor',
            ],
        },
    },
]
```


### Set up React/ReactDOM and expose your components

There are various ways of compiling react and components, to many (and fast changing) to be included in these docs. The important thing is to make sure your javascript bundle exposes `ReactDOM` globally and of course your components.


### Connecting view and template

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

    <!-- Your js includes should be included here, example:
    <script type="text/javascript" src="/static/myapp/js/react-and-react-dom.js"></script>
    <script type="text/javascript" src="/static/myapp/js/my-components.js"></script>
    -->
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

    <script type="text/javascript" src="/static/myapp/js/react-and-react-dom.js"></script>
    <script type="text/javascript" src="/static/myapp/js/my-components.js"></script>

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
