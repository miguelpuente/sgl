# from django import forms
# from django.db import models
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User, Group
# from .models import Perfil
# from apps.seguros.models import Licitacion


# class UserRegistroForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['email', 'username', 'password1',
#                   'password2']

#     def __init__(self, *args, **kwargs):
#         self.id_usuario = kwargs.pop('id_usuario', None)
#         super(UserRegistroForm, self).__init__(*args, **kwargs)

#         # Asegúrate de cargar las opciones correctas para sucursal y grupo
#         if self.id_usuario:
#             perfil = Perfil.objects.filter(user_id=self.id_usuario).first()
#             if perfil:
#                 self.fields['sucursal'].initial = perfil.sucursal
#                 self.fields['grupo'].initial = [
#                     group.name for group in perfil.user.groups.all()]

#     class Grupo(models.TextChoices):
#         COLABORADOR = 'Colaborador', 'Colaborador'
#         ENCARGADO = 'Encargado', 'Encargado'
#         GERENTE = 'Gerente', 'Gerente'
#         GENERAL = 'General', 'General'

#     email = forms.EmailField(
#         widget=forms.EmailInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Email'
#             }
#         )
#     )

#     username = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Username',
#                 'autofocus': True
#             }
#         )
#     )

#     password1 = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Contraseña'
#             }
#         ),
#         required=False
#     )

#     password2 = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Repetir Contraseña'
#             }
#         ),
#         required=False
#     )

#     sucursal = forms.ChoiceField(
#         choices=Licitacion.Sucursal.choices,
#         widget=forms.Select(
#             choices=Licitacion.Sucursal.choices,
#             attrs={
#                 'class': 'form-control',
#             }
#         )
#     )

#     grupo = forms.ChoiceField(
#         choices=Grupo.choices,
#         widget=forms.Select(
#             choices=Grupo.choices,
#             attrs={
#                 'class': 'form-control',
#             }
#         )
#     )

#     def clean_username(self):
#         username = self.cleaned_data['username']
#         if self.id_usuario:
#             if User.objects.filter(username=username).exclude(id=self.id_usuario).exists():
#                 raise forms.ValidationError(
#                     'Este nombre de usuario ya está registrado.')
#         else:
#             if User.objects.filter(username=username).exists():
#                 raise forms.ValidationError(
#                     'Este nombre de usuario ya está registrado.')
#         return username

#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if self.id_usuario:
#             if User.objects.filter(email=email).exclude(id=self.id_usuario).exists():
#                 raise forms.ValidationError(
#                     'Este correo electrónico ya está registrado.')
#         else:
#             if User.objects.filter(email=email).exists():
#                 raise forms.ValidationError(
#                     'Este correo electrónico ya está registrado.')
#         return email

#     def clean(self):
#         cleaned_data = super().clean()
#         password1 = cleaned_data.get('password1')
#         password2 = cleaned_data.get('password2')

#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError('Las contraseñas no coinciden.')

#     def save(self, commit=True):

#         user = super().save(commit=False)

#         if self.cleaned_data['password1']:
#             user.set_password(self.cleaned_data['password1'])

#         if commit:
#             user.save()

#             perfil, creado = Perfil.objects.get_or_create(user=user)
#             perfil.sucursal = self.cleaned_data['sucursal']
#             perfil.save()

#             for rol in self.Grupo.choices:
#                 if rol[0] == self.cleaned_data['grupo']:
#                     grupo, creado = Group.objects.get_or_create(name=rol[0])
#                     [Group.objects.get_or_create(
#                         name=rol[0]) for rol in self.Grupo.choices] if creado else None

#                     user.groups.clear()
#                     user.groups.add(grupo)

#         return user
