from django.forms import ModelForm
from django.contrib.auth.models import User
from bandsteps_app.models import UserProfile, Drill

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
        
    def save(self, user, commit=True):
        m = super(UserProfileForm,self).save(commit=False)
        m.user = user
        m.first_name=self.cleaned_data['first_name']
        m.last_name=self.cleaned_data['first_name']
        m.email=self.cleaned_data['email']
        m.school=self.cleaned_data['school']
        if commit:
            m.save()
        return m

class UploadFileForm(ModelForm):
    class Meta:
        model = Drill
        exclude = ('location_1','location_2','instructor',)

    def save(self,request, commit=True):
        m = super(UploadFileForm,self).save(commit=False)
        m.instructor = request.user
        m.doc=self.cleaned_data['doc']
        m.name = self.cleaned_data['name']
        if commit:
            m.save()
        return m