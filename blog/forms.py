from django import forms
from .models import News, Comments, Category

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit



class NewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         Fieldset(
    #             'first arg is the legend of the fieldset',
    #             'like_website',
    #             'favorite_number',
    #             'favorite_color',
    #             'favorite_food',
    #             'notes'
    #         ),
    #         Submit('submit', 'Submit', css_class='button white'),
    #     )


    class Meta:
        model = News
        fields = ('title',
                  'text',
                  'category',
                  'image')
        labels = {"title": 'Заголовок...',
                  "text": 'Текст...',
                  'category': "Выберите категорию...",
                  'image': 'Выберите изображение...'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80}),
                   'image': forms.ClearableFileInput(attrs={"multiple": True})}



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('comment',)
        labels = {'comment': 'Комментарий...'}
        # widgets = {'comment': forms.Textarea(attrs={'cols': 40, })}