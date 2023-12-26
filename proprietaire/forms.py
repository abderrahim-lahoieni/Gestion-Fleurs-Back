from django import forms
from core.models import Fleur

class FleurForm(forms.ModelForm):
    famille = forms.CharField(widget=forms.TextInput(), required=False)

    class Meta:
        model = Fleur
        fields = "__all__"
        exclude = ['famille']
