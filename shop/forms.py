import re

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import GIFT_COLORS, GiftPerfume, Order, Product, Review, Variant


class AddToCartForm(forms.Form):
    """One perfume + its gift. The gift depends on the volume: perfumes for 30/50 ml, Dyson for 100 ml."""
    variant = forms.ModelChoiceField(queryset=Variant.objects.filter(product__is_active=True),
                                     widget=forms.HiddenInput)
    gift_color = forms.ChoiceField(choices=GIFT_COLORS, required=False, widget=forms.RadioSelect)
    engraving = forms.CharField(max_length=20, required=False,
                                widget=forms.TextInput(attrs={'placeholder': _('Имя на корпусе (бесплатно)'),
                                                              'maxlength': 20}))
    gift_perfumes = forms.ModelMultipleChoiceField(queryset=GiftPerfume.objects.filter(is_active=True),
                                                   required=False, widget=forms.CheckboxSelectMultiple)

    def clean(self):
        data = super().clean()
        variant = data.get('variant')
        if not variant:
            return data
        if variant.gift_type == Variant.DYSON:
            if not data.get('gift_color'):
                self.add_error('gift_color', _('Выберите цвет Dyson'))
            data['gift_perfumes'] = []
        elif variant.gift_type == Variant.PERFUME:
            need, got = variant.gift_count, len(data.get('gift_perfumes') or [])
            if got != need:
                self.add_error('gift_perfumes', _('Выберите 1 парфюм в подарок') if need == 1
                               else _('Выберите %(n)s парфюма в подарок') % {'n': need})
            data['gift_color'] = data['engraving'] = ''
        else:
            data['gift_color'] = data['engraving'] = ''
            data['gift_perfumes'] = []
        return data


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'phone', 'city', 'delivery', 'payment', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('Ваше имя'), 'autocomplete': 'name'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7 (7__) ___-__-__', 'type': 'tel', 'autocomplete': 'tel'}),
            'city': forms.TextInput(attrs={'placeholder': _('Город: Алматы, Астана, Шымкент…')}),
            'delivery': forms.RadioSelect,
            'payment': forms.RadioSelect,
            'comment': forms.Textarea(attrs={'placeholder': _('Адрес, удобное время (необязательно)'), 'rows': 2}),
        }

    def clean_phone(self):
        digits = re.sub(r'\D', '', self.cleaned_data['phone'])
        if len(digits) == 11 and digits[0] in '78':
            digits = digits[1:]
        if len(digits) != 10 or digits[0] != '7':
            raise forms.ValidationError(_('Введите казахстанский номер, например +7 701 123 45 67'))
        return f'+7 {digits[:3]} {digits[3:6]} {digits[6:8]} {digits[8:]}'


class ProductChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.tr('name')


class ReviewForm(forms.ModelForm):
    rating = forms.TypedChoiceField(choices=[(i, i) for i in range(5, 0, -1)], coerce=int, initial=5,
                                    widget=forms.RadioSelect)
    product = ProductChoiceField(queryset=Product.objects.filter(is_active=True), required=False,
                                     empty_label=_('Аромат (необязательно)'))

    class Meta:
        model = Review
        fields = ['name', 'product', 'rating', 'text']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('Ваше имя')}),
            'text': forms.Textarea(attrs={'placeholder': _('Ваш отзыв — можно со смайликами 😊'), 'rows': 4}),
        }
        labels = {'name': _('Ваше имя'), 'text': _('Ваш отзыв')}

    website = forms.CharField(required=False, widget=forms.TextInput(attrs={'tabindex': '-1', 'autocomplete': 'off'}))

    def clean_text(self):
        text = self.cleaned_data['text'].strip()
        if len(text) < 3:
            raise forms.ValidationError(_('Напишите хотя бы пару слов'))
        return text[:2000]


class ReplyForm(forms.ModelForm):
    """An answer under a review: name + text, no stars."""
    parent = forms.ModelChoiceField(queryset=Review.objects.filter(is_published=True), widget=forms.HiddenInput)
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={'tabindex': '-1', 'autocomplete': 'off'}))

    class Meta:
        model = Review
        fields = ['name', 'text']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('Ваше имя')}),
            'text': forms.Textarea(attrs={'placeholder': _('Ваш ответ'), 'rows': 2}),
        }

    def clean_text(self):
        text = self.cleaned_data['text'].strip()
        if not text:
            raise forms.ValidationError(_('Напишите ответ'))
        return text[:1000]
