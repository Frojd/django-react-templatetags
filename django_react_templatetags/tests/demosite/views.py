from django.views.generic import TemplateView


class StaticReactView(TemplateView):
    template_name = "static-react.html"

    def get_context_data(self, **kwargs):
        context = super(StaticReactView, self).get_context_data(**kwargs)
        context["props"] = {
            "artist": "Tom Waits",
            "recent_album": "Bad as me",
        }
        return context
