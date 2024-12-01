from django.urls import path

from . import views#bazo ta views gia kathe endpoint

urlpatterns=[#pinakas pou tha baloume ola ta endpoints
    path("",views.home,name="home"),
    path("about/",views.about,name="about"),
    path("products/",views.products,name="products"),
    path("product/<int:id>/",views.product,name="product"),
    path("search/",views.search,name="search"),
]