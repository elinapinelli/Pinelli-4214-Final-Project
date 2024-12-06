from django.urls import path

from . import views#bazo ta views gia kathe endpoint

urlpatterns=[#pinakas pou tha baloume ola ta endpoints
    path("login/",views.login,name="login"),
    path("register/",views.register,name="register"),
    path("registerstaff/",views.register_staff,name="registerstaff"),
    path("logout/",views.logout,name="logout"),
]