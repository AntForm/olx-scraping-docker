from django.urls import path
from django.views.generic import TemplateView
from olx import views

urlpatterns = [
        path('', TemplateView.as_view(template_name="olx/home.html"), name='home'),
        path('olx/', TemplateView.as_view(template_name="olx/olx.html"), name='olx'),
        path('olx/request', views.RequestView.as_view(), name='olx_request'),
        path('olx/p_time/<int:pk>', views.PopularTime.as_view(), name='olx_p_time'),
        path('olx/p_day/<int:pk>', views.PopularDay.as_view(), name='olx_p_day'),
        ]
