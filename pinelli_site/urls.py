from django.urls import path

from . import views#bazo ta views gia kathe endpoint

urlpatterns=[#pinakas pou tha baloume ola ta endpoints
    path("",views.home,name="home"),
    path("about/",views.about,name="about"),
]