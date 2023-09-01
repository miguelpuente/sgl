from django import forms
from .models import Licitacion


class ContestadoForm(forms.ModelForm):
    class Meta:
        model = Licitacion
        fields = ['aprobado', 'fecha_contestado', 'numero_siniestro', 'aseguradora', 'perito', 'dominio', 'vehiculo',
                  'dias_demora', 'numero_presupuesto', 'cantidad_articulos', 'monto', 'localidad', 'costo_transporte']
        labels = {
            'aprobado': 'Aprobado',
            'fecha_contestado': 'Fecha contestado',
            'numero_siniestro': 'Número de Siniestro',
            'aseguradora': 'Aseguradora',
            'perito': 'Perito',
            'dominio': 'Dominio',
            'vehiculo': 'Vehiculo',
            'dias_demora': 'Días de Demora',
            'numero_presupuesto': 'N° Presupuesto',
            'cantidad_articulos': 'Cantidad de Artículos',
            'monto': 'Monto',
            'localidad': 'Localidad',
            'costo_transporte': 'Costo Transporte',
        }
        widgets = {
            'aprobado': forms.CheckboxInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'fecha_contestado': forms.SelectDateWidget(
                attrs={
                    'input_type': 'date',
                    'class': 'form-control',
                    'id': 'fecha_contestado',
                    'placeholder': '2023-12-01',
                    'required': 'true'
                }
            ),
            'numero_siniestro': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese Número de Siniestro',
                    'id': 'numero_siniestro',
                    'required': 'true'
                }
            ),
            'aseguradora': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'fecha_contestado',
                    'required': 'true'
                }
            ),
            'perito': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'perito',
                }
            ),
            'dominio': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'AB123CD o ABC123',
                    'id': 'dominio',
                    'required': 'true',
                }
            ),
            'vehiculo': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'vehiculo',
                    'required': 'true',
                }
            ),
            'dias_demora': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'dias_demora',
                    'required': 'true',
                }
            ),
            'numero_presupuesto': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese Número de Presupuesto',
                    'id': 'numero_presupuesto',
                    'required': 'true'
                }
            ),
            'cantidad_articulos': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese Cantidad de artículos',
                    'id': 'cantidad_articulos',
                    'required': 'true'
                }
            ),
            'monto': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese Monto Presupuestado',
                    'id': 'monto',
                    'required': 'true'
                }
            ),
            'localidad': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'localidad',
                    'required': 'true',
                }
            ),
            'costo_transporte': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese Costo del Transporte',
                    'id': 'costo_transporte',
                    'step': 'any',
                    'required': 'true'
                }
            )
        }


class AprobadoForm(forms.ModelForm):
    class Meta:
        model = Licitacion
        fields = ['aprobado', 'fecha_aprobado',
                  'numero_orden_compra', 'fecha_entrega_pactada']
        labels = {
            'aprobado': 'Aprobado',
            'fecha_aprobado': 'Fecha Aprobado',
            'numero_orden_compra': 'N° Orden Compra',
            'fecha_entrega_pactada': 'Fecha Entrega Pactada',
        }
        widgets = {
            'aprobado': forms.CheckboxInput(),
            'fecha_aprobado': forms.SelectDateWidget(
                attrs={
                    'input_type': 'date',
                    'class': 'form-control',
                    'id': 'fecha_aprobado',
                    'placeholder': '2023-12-01',
                    'required': 'true'
                }
            ),
            'numero_orden_compra': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese N° Orden de Compra',
                    'id': 'numero_orden_compra',
                    'required': 'true'
                }
            ),
            'fecha_entrega_pactada': forms.SelectDateWidget(
                attrs={
                    'input_type': 'date',
                    'class': 'form-control',
                    'id': 'fecha_entrega_pactada',
                    'placeholder': '2023-12-01',
                    'required': 'true'
                }
            ),
        }
