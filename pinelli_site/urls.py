from django.urls import path

from . import views#bazo ta views gia kathe endpoint

urlpatterns=[#pinakas pou tha baloume ola ta endpoints
    path("",views.home,name="home"),
    path("about/",views.about,name="about"),
    path("products/",views.products,name="products"),
    path("product/<int:id>/",views.product,name="product"), #it will take the id in order to understand for which product will put the details
    path("search/",views.search,name="search"),
    path("order/",views.order,name="order"),
    
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/checkout/', views.checkout, name='checkout'),

    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
]