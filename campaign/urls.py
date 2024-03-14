from django.urls import path
from .views import CampaignView


urlpatterns = [
        path('', CampaignView.as_view({"get": "list"})),
        path('<uuid:campaign_id>/', CampaignView.as_view({"get": "retrieve", "delete": "destroy"})),
        path('<uuid:campaign_category_id>/create/', CampaignView.as_view({"post": "create"})),
        path('<uuid:campaign_category_id>/list/', CampaignView.as_view({"get": "list_by_category"})),
        path('<uuid:campaign_id>/update', CampaignView.as_view({"put": "update"})),
        path('delete-all/', CampaignView.as_view({"delete": "destroy_all"}))
]