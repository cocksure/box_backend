from django.forms import ModelForm
from apps.production import models


class BoxModelForm(ModelForm):
    class Meta:
        model = models.BoxModel
        fields = ["name", "material", "photos", "box_size", "box_type"]