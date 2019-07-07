from django import forms
from .models import GAME_CHOICES, IndividualTournament

from bootstrap_datepicker_plus import DateTimePickerInput

GAME_CHOICES = GAME_CHOICES + [('', '---------')]


class IndividualTournamentSearchForm(forms.Form):
    game = forms.ChoiceField(label='ゲーム', choices=GAME_CHOICES, required=False)


class IndividualTournamentCreateForm(forms.ModelForm):

    class Meta:
        model = IndividualTournament
        fields = ['name', 'description', 'game', 'holdTime', 'deadTime', 'limitParticipant']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = '大会名'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['placeholder'] = '説明'
        self.fields['game'].widget.attrs['class'] = 'form-control'
        self.fields['game'].widget.attrs['placeholder'] = 'Fortnite'
        self.fields['holdTime'].widget.attrs['class'] = 'form-control'
        self.fields['holdTime'].widget = DateTimePickerInput(format='%Y-%m-%d',
                                                             options={'locale': 'ja',
                                                                      'dayViewHeaderFormat': 'YYYY年 MMMM',
                                                                      }
                                                             )
