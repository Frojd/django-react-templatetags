# Server Side Rendering

This library supports two SSR services, Hypernova and Hastur.

## Hypernova


### Installing

(We assume you got a working Hypernova SSR service running). To use hypernova you need to do the following:

1. Install `django_react_templatetags` with the `hypernova` flag.

```
pip install django_react_templatetags[hypernova]
```

2. Change SSR Service to hypernova (by adding this django setting)

```
REACT_SSR_SERVICE="django_react_templatetags.ssr.hypernova.HypernovaService"
```

3. Make sure your `REACT_RENDER_HOST` points to the batch endpoint

```
REACT_RENDER_HOST='http://react-service.test/batch
```

### Examples

- [Django React Polls with Hypernova examples](https://github.com/marteinn/django-react-polls-with-hypernova-examples) covers two ways of implementing Hypernova in Django and DRTT.

## Hastur

### Installing

To use django-react-templatetags with [Hastur](https://github.com/Frojd/Hastur) you need to do the following:

1. Install `django_react_templatetags` with the `ssr` flag.

```
pip install django_react_templatetags[ssr]
```

2. Point the right endpoint:

```
REACT_RENDER_HOST='http://hastur-service.test/
```

### How it works
It works by posting component name and props to endpoint, that returns the html rendition. Payload example:

```json
{
    "componentName": "MyComponent",
    "props": {
        "title": "my props title",
        "anyProp": "another prop"
    },
    "context": {"location": "http://localhost"},
    "static": false
}
```

You can set the context-parameter by using the `ssr_context` property on the template tag:
```html
{% react_render component="Component" ssr_context=ctx %}
```


