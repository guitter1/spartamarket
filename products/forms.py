from django import forms

from .models import Product, Comment, Hashtag

class ProductForm(forms.ModelForm):
    hashtags = forms.CharField(
    required=False,
    widget=forms.TextInput(attrs={'placeholder': '해시태그를 쉼표로 구분해서 입력하세요'})
    )
    class Meta:
        model = Product
        fields = "__all__"
        exclude=('author', 'like_users', 'views')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
        exclude=('product', 'author',)


class OrderForm(forms.Form):
    CATEGORY_CHOICES = [
        ('views', '조회수'),
        ('like_users', '찜'),
        ('pk', '최신순')
    ]

    category = forms.ChoiceField(choices=CATEGORY_CHOICES, initial='pk', required=False)

class HashtagForm(forms.ModelForm):
    class Meta:
        model=Hashtag
        fields = "__all__"