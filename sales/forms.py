from django import forms
from sales.models import Materials, Coming, Expenses, Stock


class ComingForm(forms.ModelForm):
    class Meta:
        model = Coming
        fields = ['stock', 'material', 'quantity', 'price']


class StockFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(StockFilterForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['stock'].queryset = Stock.objects.filter(users=user)

    stock = forms.ModelChoiceField(queryset=Stock.objects.none(), required=False, empty_label="Все склады")
