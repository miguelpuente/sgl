from django.contrib import admin
from apps.users.models import Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'sucursal','imagen')
    list_display_links = ('pk', 'user', 'sucursal')
    list_editable = ('imagen',)

    search_fields = (
        'user__email',
        'user__username',
        'user__first_name',
        'users__last_name',
    )

    list_filter = (
        'user__is_active',
        'user__is_staff',
        'modificado',
    )

    fieldsets = (
        ('Perfil', {
            'fields': (('user', 'sucursal', 'imagen'),),
        }),
        ('Extra info', {
            'fields': (('modificado'),),
        })
    )

    readonly_fields = ('modificado',)
