from . import views
from django.urls import path

urlpatterns = [
    path("products/get/all/", views.getAllProducts),
    path("products/get/ids/", views.getProductsById),
    path("products/add/", views.addProduct),
    path("products/update/", views.updateProduct),
    path("products/delete/<int:id>/", views.deleteProduct),
    
    path("orders/get/all/", views.getAllOrders),
    path("orders/add/", views.addOrder),
    path("orders/complete/<int:id>/", views.completeOrder),
    path("orders/delete/<int:id>/", views.deleteOrder),
    
    path("files/add/", views.addFile),

    path("dashboard/", views.getDashboard),
    path("email/set/<str:newEmail>/", views.setEmail),
    path("statistics/", views.statistics)
]