from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, ListView, UpdateView
# from .forms import UserRegistroForm
from .models import Perfil


# class UserCreateView(UserPassesTestMixin, CreateView):
#     form_class = UserRegistroForm
#     template_name = 'user/registro.html'
#     success_url = reverse_lazy('auth:listado')
#     login_url = reverse_lazy('auth:login')

#     def test_func(self):
#         return self.request.user.is_authenticated and self.request.user.is_superuser and self.request.user.is_active

#     def form_valid(self, form):
#         try:
#             return super().form_valid(form)
#         except IntegrityError as e:
#             if 'UNIQUE constraint' in str(e):
#                 form.add_error(
#                     None, 'Este nombre de usuario o correo electrónico ya está registrado.')
#             else:
#                 form.add_error(
#                     None, 'Ha ocurrido un error durante el registro. Por favor, inténtalo de nuevo.')
#             return self.form_invalid(form)

#     def form_invalid(self, form):
#         # Agrega un mensaje de error al contexto antes de renderizar el template
#         error_messages = form.errors
#         return render(self.request, self.template_name, {'form': form, 'error_messages': error_messages})


class UserDetailView(UserPassesTestMixin, DetailView):
    model = Perfil
    template_name = 'user/detalle.html'
    context_object_name = 'usuario'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser and self.request.user.is_active


# class UserUpdateView(UserPassesTestMixin, UpdateView):
#     model = User
#     form_class = UserRegistroForm
#     template_name = 'user/editar.html'
#     success_url = reverse_lazy('auth:listado')
#     login_url = reverse_lazy('auth:login')

#     def test_func(self):
#         return self.request.user.is_authenticated and self.request.user.is_superuser and self.request.user.is_active

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['id_usuario'] = self.object.id if self.object else None
#         return kwargs

#     def form_valid(self, form):
#         try:
#             return super().form_valid(form)
#         except IntegrityError as e:
#             if 'UNIQUE constraint' in str(e):
#                 form.add_error(
#                     None, 'Este nombre de usuario o correo electrónico ya está registrado.')
#             else:
#                 form.add_error(
#                     None, 'Ha ocurrido un error durante la actualización. Por favor, inténtalo de nuevo.')
#             return self.form_invalid(form)

#     def form_invalid(self, form):
#         # Agrega un mensaje de error al contexto antes de renderizar el template
#         error_messages = form.errors
#         return render(self.request, self.template_name, {'form': form, 'error_messages': error_messages})


class UserListView(LoginRequiredMixin, ListView):
    model = Perfil
    template_name = 'user/manager.html'
    context_object_name = 'usuarios'


class LoginFormView(LoginView):
    template_name = 'pages/user/login.html'
    success_url = reverse_lazy('seguros:inicio')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('seguros:inicio')
        return super().dispatch(request, *args, **kwargs)


class SalirView(LoginRequiredMixin, LogoutView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('auth:login'))
