from django import forms
from .models import Autorizacion, EPP




class AutorizacionForm(forms.ModelForm):
    class Meta:
        model = Autorizacion
        fields = ['personal_bodega', 'epp_solicitado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['epp_solicitado'].queryset = EPP.objects.all()


class EPPForm(forms.ModelForm):
    class Meta:
        model = EPP
        fields = ['nombre']
        labels = {'nombre': 'Nombre del EPP'}

class SubirDocumentoFirmadoForm(forms.ModelForm):
    class Meta:
        model = Autorizacion
        fields = ['documento_firmado']