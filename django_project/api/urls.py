# -*- coding: utf-8 -*-
from django.conf.urls import include, url

from api.api_views.v1 import ApiVersion2
from api.views.enrollment_form import EnrollmentFormView

api_urls = [
    url(r'v3/', include('api.urls_v3')),
    url(r'v2/', ApiVersion2.as_view()),
    url(r'v1/', ApiVersion2.as_view()),
    url(r'^', include('api.urls_schema')),
]
urlpatterns = [
    url(r'^api/', include(api_urls)),
    url(
        r'^enrollment/form', EnrollmentFormView.as_view(),
        name='enrollment-form'
    ),
]
