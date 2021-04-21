from django.urls import path
from . import views

app_name = "Album"  # 为app设置命名空间，方便{% url "Album:..."}区分

urlpatterns = [
    path("",views.index,name="index"),
    path("index/",views.index,name="index"),
    path("login/",views.login,name="login"),
    path("signup/",views.signup,name="signup"),
    path("loginout/",views.loginout,name="loginout"),
    path("ajax_val/",views.ajax_val,name="ajax_val"),
]
