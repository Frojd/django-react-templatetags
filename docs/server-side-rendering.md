# Server Side Rendering

This library supports SSR (Server Side Rendering) throught third-part library [Hastur](https://github.com/Frojd/Hastur).

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

`REACT_RENDER_HOST` needs to be defined to enable communication with service.

You can set the context-parameter by using the `ssr_context` property on the template tag:
```html
{% react_render component="Component" ssr_context=ctx %}
```
