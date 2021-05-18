from django.utils.text import slugify
from django.core.files.base import ContentFile
from django import forms
from .models import Image
from urllib import request


class ImageCreateForm(forms.ModelForm):

    url = forms.CharField(widget=forms.HiddenInput())
    title=forms.CharField(widget=forms.TextInput(attrs={'class':'mb-2','placeholder':'Title'}))
    description=forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Description'}))

    class Meta:
        model = Image
        fields = ['title', 'url', 'description']

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg','png']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extensions.')
        return url

    def save(self, force_insert=False,force_update=False,commit=True):
        
        image = super(ImageCreateForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = f"{slugify(image.title)}.{image_url.rsplit('.', 1)[1].lower()}"

        # download image from the given URL
        response = request.urlopen(image_url)
        image.image.save(image_name,ContentFile(response.read()),save=False)

        if commit:
            image.save()
        return image
