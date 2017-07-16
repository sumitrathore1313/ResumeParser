from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView
from .views import DetailsView 
from .views import FileUploadView

urlpatterns = {
    url(r'^bucketlists/$', CreateView.as_view(), name="create"),
    url(r'^bucketlists/(?P<pk>[0-9]+)/$',
        DetailsView.as_view(), name="details"),
    url(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view())
}

urlpatterns = format_suffix_patterns(urlpatterns)