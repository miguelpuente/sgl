from django import forms
from apps.auto.models import Modelo
from apps.direccion.models import DatoEntrega, Localidad, Provincia
from .models import Licitacion, Demora, Aseguradora, Perito

class LicitacioForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Obtén la instancia de datos_entrega actual
        if self.instance.datos_entrega:
            self.fields['localidad'].initial = self.instance.datos_entrega.localidad
            self.fields['provincia'].initial = self.instance.datos_entrega.localidad.provincia

    class Meta:
        model = Licitacion
        fields = ['numero_siniestro', 'user', 'sucursal', 'aseguradora', 'perito', 'demora', 'vehiculo', 'dominio', 'numero_presupuesto', 'cantidad_articulos', 'monto','costo_transporte', 'datos_entrega', 'terminado']

    numero_siniestro = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'autocomplete': False,
                'required': True
            }
        )
    )
    demora = forms.ModelChoiceField(
        queryset= Demora.objects.filter(activo=True),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'required': True
            }
        )
    )
    numero_presupuesto = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'autocomplete': False,
                'autofocus': True,
                'required': True
            }
        )
    )
    cantidad_articulos = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'autocomplete': False,
                'required': True
            }
        )
    )
    monto = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'autocomplete': False,
                'required': True
            }
        )
    )
    vehiculo = forms.ModelChoiceField(
        queryset= Modelo.objects.filter(activo=True),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'required': True
            }
        )
    )
    dominio = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'autocomplete': False,
                'maxlength': 7,
                'minlength': 6,
                'autocomplete': False,
                'required': True
             }
        )
    )
    aseguradora = forms.ModelChoiceField(
        queryset= Aseguradora.objects.filter(activo=True),
        widget=forms.Select(
            attrs={
                'class': 'form-control select2',
                'required': True
            }
        )
    )

    perito = forms.ModelChoiceField(
        queryset= Perito.objects.filter(activo=True),
        widget=forms.Select(
            attrs={
                'class': 'form-control select2'
            }
        )
    )

    costo_transporte = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'autocomplete': False,
                'required': True
            }
        )
    )
    provincia = forms.ModelChoiceField(
        queryset= Provincia.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control select2',
                'required': True
            }
        )
    )
    localidad = forms.ModelChoiceField(
        queryset= Localidad.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control select2',
                'required': True
            }
        )
    )
    terminado = forms.BooleanField(
        widget = forms.CheckboxInput(
            attrs={
                'class' : 'custom-control-input',
                'id' : 'customSwitch3',
            }
        ),
        required= False
    )

    def save(self, commit=True):
        data={}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data