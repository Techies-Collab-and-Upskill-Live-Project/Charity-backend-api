from django.urls import path
from .views import CampaignCategoryView


urlpatterns = [
        path('create/', CampaignCategoryView.as_view({"post": "create"})),
        path('list/', CampaignCategoryView.as_view({"get": "list"})),
        path('<uuid:pk>/', CampaignCategoryView.as_view({"get": "retrieve"})),
        path('update/<uuid:pk>/', CampaignCategoryView.as_view({"put": "update"})),
        path('delete/<uuid:pk>/', CampaignCategoryView.as_view({"delete": "destroy"})),
]
