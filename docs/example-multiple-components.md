# Adding multiple components

You can also have multiple components in the same template

This view...

```python
from django.shortcuts import render

def menu_view(request):
    return render(request, 'myapp/index.html', {
        'menu_data': {
            'example': 1,
        },
        'title_data': 'My title',
        'footer_data': {
            'credits': 'Copyright Company X'
        }
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
            {% react_render component="Title" prop_title=title %}
            {% react_render component="Footer" props=footer_data %}
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
        <main>
            <div id="Title_405190d92bbc4d00b9e3376522982728"></div>
        </main>
        <footer>
            <div id="Footer_405190d92bbc4d00b9e3376522982728"></div>
        </footer>
    </body>

    <script id="Menu_405190d92bbc4d00b9e3376522982728_data" type="application/json">{"example": 1}</script>
    <script>
        ReactDOM.render(
            React.createElement(
                Menu,
                JSON.parse(document.getElementById("Menu_405190d92bbc4d00b9e3376522982728_data").textContent)
            ),
            document.getElementById('Menu_405190d92bbc4d00b9e3376522982728')
        );
    </script>
    <script id="Title_405190d92bbc4d00b9e3376522982728_data" type="application/json">{"title": "My title"}</script>
    <script>
        ReactDOM.render(
            React.createElement(
                Title,
                JSON.parse(document.getElementById("Title_405190d92bbc4d00b9e3376522982728_data").textContent)
            ),
            document.getElementById('Title_405190d92bbc4d00b9e3376522982728')
        );
    </script>
    <script id="Footer_405190d92bbc4d00b9e3376522982728_data" type="application/json"> {"credits": "Copyright Company X"}</script>
    <script>
        ReactDOM.render(
            React.createElement(
                Footer,
                JSON.parse(document.getElementById("Footer_405190d92bbc4d00b9e3376522982728_data").textContent)
            ),
            document.getElementById('Footer_405190d92bbc4d00b9e3376522982728')
        );
    </script>
</html>
```
