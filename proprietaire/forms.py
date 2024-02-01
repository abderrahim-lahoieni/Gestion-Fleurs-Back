from django import forms
from core.models import Fleur, Fichesoin, Famille, Magasin, Parfum, Bouquet

class FleurForm(forms.ModelForm):

    class Meta:
        model = Fleur
        fields = "__all__" 
        exclude=['code']                

class FichesoinForm(forms.ModelForm):

    class Meta:
        model = Fichesoin
        fields = "__all__"

class FamilleForm(forms.ModelForm):

    class Meta:
        model = Famille
        fields = "__all__" 

class MagasinForm(forms.ModelForm):

    class Meta:
        model = Magasin
        fields = "__all__"

class ParfumForm(forms.ModelForm):

    class Meta:
        model = Parfum
        fields = "__all__"  
        exclude=['code']              
       
class BouquetForm(forms.ModelForm):

    class Meta:
        model = Bouquet
        fields = "__all__"  
        exclude=['code']                         
              
