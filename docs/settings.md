# Settings

### General

- `REACT_COMPONENT_PREFIX`: Adds a prefix to your React.createElement include, if you want to retrive your components from somewhere else then the global scope. (Default is `""`).
    - Example using (`REACT_COMPONENT_PREFIX="Cookie."`) will look for components in a global scope object named `Cookie`.
    - ...Becomes: `React.createElement(Cookie.MenuComponent, {})`
- `REACT_RENDER_TAG_MANAGER`: This is a advanced setting that lets you replace our tag parsing rules (ReactTagManager) with your own. (Default is `""`)
    - Example: `"myapp.manager.MyReactTagManager"`

### SSR (Server Side Rendering)

- `REACT_RENDER_HOST`: Which endpoint SSR requests should be posted at. (Default is `""`)
    - Example: `http://localhost:7000/render-component/`
    - The render host is a web service that accepts a post request and and renders the component to HTML. (This is what our [Hastur](https://github.com/Frojd/hastur) service does)
- `REACT_RENDER_TIMEOUT`: Timeout for SSR requests, in seconds. (Default is `20`)
- `REACT_RENDER_HEADERS`: Override the default request headers sent to the SSR service. Default: `{'Content-type': 'application/json', 'Accept': 'text/plain'}`.
    - Example: `REACT_RENDER_HEADERS = {'Authorization': 'Basic 123'}`
- `REACT_SSR_SERVICE`: Replace the SSR Service with your own, can be useful if you have custom needs or our structure does not fit your use case. (Default is `django_react_templatetags.ssr.default.SSRService`).
