from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import UserDetailView, UserListView, LoginFormView, SalirView

app_name = 'apps.users'

urlpatterns = [

    # path(
    #     route='registro/',
    #     view=UserCreateView.as_view(),
    #     name='registro'
    # ),
    path(
        route='detalle/<uuid:pk>/',
        view=login_required(UserDetailView.as_view()),
        name='detalle'
    ),
    # path(
    #     route='editar/<int:pk>/',
    #     view=UserUpdateView.as_view(),
    #     name='editar'
    # ),
    path(
        route='listado/',
        view=login_required(UserListView.as_view()),
        name='listado'
    ),
    path(
        route='login/',
        view=LoginFormView.as_view(),
        name='login'
    ),
    path(
        route='salir/',
        view=login_required(SalirView.as_view()),
        name='salir'
    ),
]
