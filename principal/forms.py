from django import forms
from .models import Post


class PosteoForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["titulo", "descripcion", "categoria"]


# este forms.py es nuevo
