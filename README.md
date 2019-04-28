[![Build Status](https://travis-ci.org/Frojd/django-react-templatetags.svg?branch=master)](https://travis-ci.org/Frojd/django-react-templatetags)
[![PyPI version](https://badge.fury.io/py/django_react_templatetags.svg)](https://badge.fury.io/py/django_react_templatetags)

![Django-React-Templatetags](https://raw.githubusercontent.com/frojd/django-react-templatetags/develop/img/django-react-templatetags-logo.png)

# Django-React-Templatetags

This django library allows you to add React (16+) components into your django templates.


## Features

- Include react components using django templatetags
- Unlimited amount of components in one view
- Support custom models (that is from the beginning not json-serializable)
- Server side rendering


## Installation

Install the library with pip:

```
$ pip install django_react_templatetags
```


## Where to go from here?

You should first read [Getting started](https://github.com/Frojd/django-react-templatetags/blob/develop/docs/getting-started.md), then go through these topics:
- [Settings](https://github.com/Frojd/django-react-templatetags/blob/develop/docs/settings.md)
- [Adding a single component](https://github.com/Frojd/django-react-templatetags/blob/develop/<Paste>docs/example-single-component.md)
- [Adding multiple components](https://github.com/Frojd/django-react-templatetags/blob/develop/docs/example-multiple-components.md)
- [Example application](https://github.com/Frojd/django-react-templatetags/blob/develop/docs/example-application.md)
- [Working with models](https://github.com/Frojd/django-react-templatetags/blob/develop/docs/working-with-models.md)
- [Server side rendering](https://github.com/Frojd/django-react-templatetags/blob/develop/docs/server-side-rendering.md)
- [FAQ](https://github.com/Frojd/django-react-templatetags/blob/develop/docs/faq.md)


## Tests

This library include tests, just run `python runtests.py`

You can also run separate test cases: `python runtests.py tests.test_filters.ReactIncludeComponentTest`


## Contributing

Want to contribute? Awesome. Just send a pull request.


## License

Django-React-Templatetags is released under the [MIT License](http://www.opensource.org/licenses/MIT).
