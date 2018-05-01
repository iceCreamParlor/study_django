from django import forms
from .models import Item
from restaurant.models import RestaurantLocation

class ItemForm(forms.ModelForm):
    class Meta:
        model=Item
        fields=[
            'restaurant',
            'name',
            'contents',
            'excludes',
            'public',
        ]
    def __init__(self, user=None, *args, **kwargs): # 로그인한 사용자가 입력한 음식점만 출력하기 
        #print(kwargs.pop('user'))
        print(user)
        print(kwargs)
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['restaurant'].queryset= RestaurantLocation.objects.filter(owner=user).exclude(item__isnull=False)