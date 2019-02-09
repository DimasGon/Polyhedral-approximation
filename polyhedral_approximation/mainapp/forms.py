from django import forms
from math import pi

class InputForm(forms.Form):

    phi1 = forms.FloatField(label='Угол фи в радианах для первой точки', required=True)
    phi2 = forms.FloatField(label='Угол фи в радианах для второй точки', required=True)
    phi3 = forms.FloatField(label='Угол фи в радианах для третьей точки', required=True)

    def clean(self):
        cleaned_data = super().clean()
        phi1 = cleaned_data['phi1']
        phi2 = cleaned_data['phi2']
        phi3 = cleaned_data['phi3']
        if abs(phi1 - phi2) < pi and abs(phi1 - phi3) < pi and abs(phi2 - phi3) < pi or\
            abs(phi1 - phi2) > pi and abs(phi1 - phi3) > pi or abs(phi2 - phi1) > pi and abs(phi2 - phi3) > pi or\
            abs(phi3 - phi1) > pi and abs(phi3 - phi2) > pi:
            raise forms.ValidationError(
                'Все три точки лежат на полуокружности!\nЗамкнуть внешнюю аппроксимацию не получится!'
            )
