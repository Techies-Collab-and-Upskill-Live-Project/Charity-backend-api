from django.urls import path
from .views import DonationsView


urlpatterns = [
        path('create/', DonationsView.as_view({"post": "create"})),
        path('list/', DonationsView.as_view({"get": "list"})),
        path('<uuid:campaign_id>/', DonationsView.as_view({"get": "retrieve"})),
        path('delete/<donation_id>/', DonationsView.as_view({"delete": "destroy"})),
]