from django import forms
from apps.auto.models import Modelo
from apps.direccion.models import DatoEntrega, Localidad, Provincia
from .models import Licitacion, Aprobada, Demora, Aseguradora, Perito, Preparada, Taller, Transporte

class LicitacioForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.datos_entrega:
            self.fields['localidad'].initial = self.instance.datos_entrega.localidad
            self.fields['provincia'].initial = self.instance.datos_entrega.localidad.provincia

    class Meta:
        model = Licitacion
        fields = ['numero_siniestro', 'user', 'sucursal', 'aseguradora', 'perito', 'demora', 'vehiculo', 'dominio', 'numero_presupuesto', 'cantidad_articulos', 'monto','costo_transporte', 'terminado', 'datos_entrega' ]

    numero_siniestro = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'step': 'any',
                'maxlength': 20,
                'decimal_places': 0,
                'autocomplete': False,
            }
        )
    )

    def clean_numero_siniestro(self):
        numero = self.cleaned_data.get('numero_siniestro')
        if numero is not None and numero < 0:
            raise forms.ValidationError('El número debe ser positivo.')
        return numero

    demora = forms.ModelChoiceField(
        queryset= Demora.objects.filter(activo=True),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    numero_presupuesto = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'step': 'any',
                'maxlength': 20,
                'decimal_places': 0,
                'autocomplete': False,
                'autofocus': True,
            }
        )
    )

    def clean_numero_presupuesto(self):
        numero = self.cleaned_data.get('numero_presupuesto')
        if numero is not None and numero < 0:
            raise forms.ValidationError('El número debe ser positivo.')

        return numero

    cantidad_articulos = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'step': 'any',
                'maxlength': 4,
                'decimal_places': 0,
                'autocomplete': False,
            }
        )
    )

    def clean_cantidad_articulos(self):
        numero = self.cleaned_data.get('cantidad_articulos')
        if numero is not None and numero < 0:
            raise forms.ValidationError('El número debe ser positivo.')
        return numero

    monto = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'step': 'any',
                'maxlength': 10,
                'decimal_places': 2,
                'autocomplete': False,
            }
        )
    )

    def clean_monto(self):
        numero = self.cleaned_data.get('monto')
        if numero is not None and numero < 0:
            raise forms.ValidationError('El número debe ser positivo.')
        return numero

    vehiculo = forms.ModelChoiceField(
        queryset= Modelo.objects.filter(activo=True),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    dominio = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '"ABC123" o "AB123CD"',
                'maxlength': 7,
                'minlength': 6,
                'autocomplete': False,
             }
        )
    )

    aseguradora = forms.ModelChoiceField(
        queryset= Aseguradora.objects.filter(activo=True),
        widget=forms.Select(
            attrs={
                'class': 'form-control select2',
            }
        )
    )

    perito = forms.ModelChoiceField(
        queryset= Perito.objects.filter(activo=True),
        widget=forms.Select(
            attrs={
                'class': 'form-control select2',
            }
        ),
        required=False
    )

    costo_transporte = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'step': 'any',
                'maxlength': 10,
                'decimal_places': 2,
                'autocomplete': False,
            }
        )
    )

    def clean_costo_transporte(self):
        numero = self.cleaned_data.get('costo_transporte')
        if numero is not None and numero < 0:
            raise forms.ValidationError('El número debe ser positivo.')
        return numero

    provincia = forms.ModelChoiceField(
        queryset= Provincia.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control select2',
                'required': True,
            }
        )
    )

    localidad = forms.ModelChoiceField(
        queryset= Localidad.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control select2',
                'required': True,
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


class AprobadaForm(forms.ModelForm):
    class Meta:
        model = Aprobada
        fields = ['fecha_aprobado', 'numero_orden_compra', 'numero_nota_pedido', 'taller', 'transporte', 'terminado']

    fecha_aprobado = forms.DateField(
        widget= forms.DateInput(
            format='%m-%d-%Y',
            attrs={
                'class': 'form-control',
                'type': 'date',
                'autofocus': True,
            }
        ),
        required= True
    )

    def clean_fecha_aprobado(self):
        fecha_aprobado = self.cleaned_data['fecha_aprobado']

        if fecha_aprobado is None:
            raise forms.ValidationError('Este campo es obligatorio.')

        return fecha_aprobado

    numero_orden_compra = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'step': 'any',
                'maxlength': 20,
                'decimal_places': 0,
                'autocomplete': False,
            }
        )
    )

    def clean_numero_orden_compra(self):
        numero = self.cleaned_data.get('numero_orden_compra')
        if numero is not None and numero < 0:
            raise forms.ValidationError('El número debe ser positivo.')

        return numero

    numero_nota_pedido = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'step': 'any',
                'maxlength': 20,
                'decimal_places': 0,
                'autocomplete': False,
            }
        ),
        required = False
    )

    def clean_numero_nota_pedido(self):
        numero = self.cleaned_data.get('numero_nota_pedido')
        if numero is not None and numero < 0:
            raise forms.ValidationError('El número debe ser positivo.')

        return numero

    taller = forms.ModelChoiceField(
        queryset= Taller.objects.filter(activo=True),
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
        required=False
    )

    transporte = forms.ModelChoiceField(
        queryset= Transporte.objects.filter(activo=True),
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
        required=True
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

class PreparadaForm(forms.ModelForm):
    class Meta:
        model = Preparada
        fields = ['cantidad_articulos_listos', 'comentario', 'terminado']

    cantidad_articulos_listos = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'step': 'any',
                'maxlength': 4,
                'decimal_places': 0,
                'autocomplete': False,
            }
        ),
        required = True
    )

    def cantidad_articulos_listos(self):
        numero = self.cleaned_data.get('cantidad_articulos_listos')
        if numero is not None and numero < 0:
            raise forms.ValidationError('El número debe ser positivo.')
        return numero
    
    comentario = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'autocomplete': False,
            }
        ),
        required=False
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

    def clean(self):
        cleaned_data = super().clean()
        cantidad_articulos_listo = cleaned_data.get('cantidad_articulos_listos')
        comentario = cleaned_data.get('comentario')
        terminado = cleaned_data.get('terminado')

        articulos = self.instance.aprobada.licitacion.cantidad_articulos
        
        if terminado and (
        (cantidad_articulos_listo is not None and cantidad_articulos_listo != articulos and cantidad_articulos_listo <= 0) or
        not comentario):
            self.add_error('comentario', forms.ValidationError(
            f'Para cambiar "Lista Enviar", "Artículos Listos" debe ser igual a {articulos}. Si desea enviar con faltante, agregue un comentario'
        ))

        return cleaned_data

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