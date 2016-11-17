[![Build Status](https://travis-ci.org/Frojd/django-react-templatetags.svg?branch=master)](https://travis-ci.org/Frojd/django-react-templatetags)
[![PyPI version](https://badge.fury.io/py/django-react-templatetags.svg)](https://badge.fury.io/py/django-react-templatetags)

# Django-React-Templatetags

This extension allows you to add React components into your django templates.


## Requirements

- Python 2.7 / Python 3.4 / PyPy
- Django 1.8+


## Installation

Install the library with pip:

```
$ pip install django_react_templatetags
```


## Quick Setup

Make sure django_react_templatetags is added to your `INSTALLED_APPS`.

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

This should be enough to get started.


## Usage

1. Load the `{% load react %}`
2. Insert component anywhere in your template: `{% react_render component="Component" data=my_data %}`. This will create a dom placeholder.
3. Put `{% react_print %}` in the end of your template. (This will output the ReactDom.render javascript).


## Full example

This template:

```
{% load react %}
<html>
    <head>...</head>

    <body>
        <nav>
            {% react_render component="Menu" data=menu_data %}
        </nav>
    </body>

    {% react_print %}
</html>
```

Will transform into this:

```
{% load react %}
<html>
    <head>...</head>

    <body>
        <nav>
            <div id="Menu_1"></div>
        </nav>
    </body>

    <script>
        ReactDOM.render(
            React.createElement(Menu, {'example', 1}),
            document.getElementById('Menu_405190d92bbc4d00b9e3376522982728')
        );
    </script>
</html>
```


## Settings

- `REACT_COMPONENT_PREFIX`: Adds a prefix to your React.createElement include.
    - Example using (`REACT_COMPONENT_PREFIX="Cookie."`)
    - ...Becomes: `React.createElement(Cookie.MenuComponent, {})`


## Q&A

### Question: How do I override the markup generated by `react_print`?

Simple! Just override the template `react_print.html`

### Question: This library only contains templatetags, where is the react js library?

This library only covers the template parts (that is: placeholder and js render).

### Question: I dont like the autogenerated element id, can I supply my own element?

Sure! Just add the param `identifier="yourid"` in `react_render`.

Example:
```
{% react_render component="Component" identifier="yourid" %}
```

...will print 
```html
<div id="yourid"></div>
```

### Question: How do I apply my own css class to the autogenerated element?
    
Add `class="yourclassname"` to your `{% react_render ... %}`. 
    
Example: 
```html
{% react_render component="Component" class="yourclassname" %}
```

...will print 
```html
<div id="Component_405190d92bbc4d00b9e3376522982728" class="yourclassname"></div>j
```

### Question: I want to pass the component name as a variable, is that possible?

Yes! Just remove use a variable in your react_render:

Example:
```
{% react_render component=component_variable %}
```


## Tests

This library include tests, just run `python runtests.py`

You can also run separate test cases: `runtests.py tests.ReactIncludeComponentTest`


## Contributing

Want to contribute? Awesome. Just send a pull request.


## License

Django-React-Templatetags is released under the [MIT License](http://www.opensource.org/licenses/MIT).

