from django.urls import path
from . import views

urlpatterns = [
    path("products_list/", views.ProductListAPIView.as_view(), name="product_list"),
    path(
        "products_create/", views.ProductCreateAPIView.as_view(), name="product_create"
    ),
    path("group_list/", views.ListGroupAPIView.as_view(), name="group_list"),
    path("group_create/", views.CreateGroupAPIView.as_view(), name="group_create"),
    path(
        "group_add/<int:product_id>/<int:user_id>/",
        views.GroupAddAPIView.as_view(),
        name="group_add",
    ),
]
