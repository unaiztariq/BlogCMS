from django import forms
from .models import Post,Category
from ckeditor.widgets import CKEditorWidget 

class PostForm(forms.ModelForm):
    category= forms.CharField(max_length=100)

    


    class Meta:
        model = Post

        fields=["title","status","category","tags","content"]

        widgets ={
            "content": CKEditorWidget()
        }
    
    def clean_category(self):

        category_name = self.cleaned_data["category"]
        try:
            category= Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            category= Category.objects.create(name=category_name)

        return category

        