from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "discount": forms.NumberInput(attrs={"class": "form-control"}),
            "stock": forms.NumberInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        category = self.initial.get("category") or self.data.get("category")
        # if category != "bouquet":
        #     self.fields.pop("size", None)
        #     self.fields.pop("seasonality", None)
        #     self.fields.pop("style", None)
        #     self.fields.pop("flower_ingredients", None)


class ProductFilterForm(forms.Form):
    flower_ingredients = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Flower Type"
    )
    size = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    seasonality = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    style = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Product

        self.fields['flower_ingredients'].choices = [
            (f.name, f.name) for f in Product.objects.filter(category='flower')
        ]
        self.fields['size'].choices = [
            (s, s) for s in Product.objects.exclude(size__isnull=True).values_list('size', flat=True).distinct()
        ]
        self.fields['seasonality'].choices = [
            (s, s) for s in Product.objects.exclude(seasonality__isnull=True).values_list('seasonality', flat=True).distinct()
        ]
        self.fields['style'].choices = [
            (st, st) for st in Product.objects.exclude(style__isnull=True).values_list('style', flat=True).distinct()
        ]