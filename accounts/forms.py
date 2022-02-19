from django.forms import ModelForm
from .models import Producer, Company, Loading, Truck
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        exclude = ['user']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoadingForm(ModelForm):
    class Meta:
        model = Loading
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(LoadingForm, self).__init__(*args, **kwargs)
        if self.company:
            self.fields['truck'].queryset = Truck.objects.filter(producer__company=self.company.id)
