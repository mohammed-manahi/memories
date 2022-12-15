import requests
from django import forms
from django.utils.text import slugify
from django.core.files.base import ContentFile
from core.models import Image


class ImageCreateForm(forms.ModelForm):
    # Create a from for image creation which gets the url of the image to share with users
    class Meta:
        model = Image
        fields = ["title", "url", "description"]
        # URL field is hidden since the js will handel getting the image url from external resources
        widgets = {"url": forms.HiddenInput, }

    def clean_url(self):
        # Use clean_field_name to validate that the url is for an image when the is_valid method is called
        url = self.cleaned_data["url"]
        valid_extensions = ["jpg", "jpeg", "png"]
        # rsplit splits by the dot to a list and the extension is the second slice [1]
        extension = url.rsplit(".", 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError("The fetched URL contains no valid image extension")
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        # Override form save method to download the image by its url
        image = super().save(commit=False)
        image_url = self.cleaned_data["url"]
        name = slugify(image.title)
        extension = image_url.rsplit(".", 1)[1].lower()
        image_name = f"{name}.{extension}"
        response = requests.get(image_url)
        # Get the image in media directory
        image.image.save(image_name, ContentFile(response.content), save=False)
        # Only save image when commit is true
        if commit:
            image.save()
        return image
