from django import forms

from catalog.models import Product


class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        labels = {
            "name":"",
            "price":"",
            "description":"",
            "image":"",
            "category":"",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "inp", "type": "text", "id": "name"}),
            "price": forms.TextInput(attrs={"class": "inp", "type": "number", "id": "price", "pattern": "^[0-9]+$"}),
            "description": forms.Textarea(attrs={"class": "inp", "type": "textarea", "id": "description", "style":"width: 40vw;height: 30vh"}),
            "category": forms.Select(attrs={"class": "inp", "id": "category"}),
        }