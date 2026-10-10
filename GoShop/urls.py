from django.urls import path
from .views import *

urlpatterns=[
    path('',Home.as_view(),name='Home'),
    path('Category/',Category_View.as_view(),name='Category'),
    path('Product/<str:name>',Product_View.as_view(),name='product'),
    path('product_page/<int:id>',product_page.as_view(),name='Selected_Product'),
    path('all_products/',product_all.as_view(),name='all_products'),
    path('signup/',SignUp_Page.as_view(),name='signup'),
    path('login/',login_view.as_view(),name='login'),
    path('lagout/',logout_view.as_view(),name='logout'),
    path('add_Cart/<int:id>',Cart_page.as_view(),name='add_Cart'),
    path('toggle_like/<int:id>',toggle_like.as_view(),name='toggle_like'),
    path('favourate_view/',favourate_view.as_view(),name='favourate_view'),
    path('order_page/',order_page.as_view(),name='order_page'),
    path('cart_delete/<int:id>',cart_delete.as_view(),name='cart_delete'),
    path('sheping_View/',ShepingView.as_view(),name='sheping_View'),
    path('tracking_page/',tracking_page.as_view(),name='tracking_page'),
    path('delete_tracking/<int:id>',tracking_cancle.as_view(),name='tracking_cancle'),
    # path('Delivery/',Delivery.as_view(),name='Delivery'),
    path('contact/', Contact_Page_View.as_view(), name='contact'),
    path('Searched_item/',Searched_item.as_view(),name='Searched_item'),

]

