from django.views.generic import DetailView, TemplateView

from models import Server

class ServerDetailView(DetailView):

    context_object_name = "server"
    model = Server

    def get_context_data(self, **kwargs):
        context = super(ServerDetailView, self).get_context_data(**kwargs)
        return context

class VersionDetailView(TemplateView):
    template_name = "teeworlds_monitor/version_detail.html"
    def get_context_data(self, **kwargs):
        context = super(VersionDetailView, self).get_context_data(**kwargs)
        context["version"] = kwargs["version"]
        return context