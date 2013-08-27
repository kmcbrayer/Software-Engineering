from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    school = models.CharField(max_length=200)
    intstrument = models.CharField(max_length=200)
    
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            profile, created = UserProfile.objects.get_or_create(user=instance)
            
    post_save.connect(create_user_profile, sender=User)
    
    def __unicode__(self):
        return self.user.username
    
class Drill(models.Model):
    name = models.CharField(max_length=30)
    location_1 = models.CharField(max_length=50, null=True,blank=True)
    location_2 = models.CharField(max_length=50, null=True,blank=True)
    instructor= models.ForeignKey(User)

    def __unicode__(self):
        return self.name
    
    def set_location(self, lat,long):
        #use google to get la
        return
    
class Set(models.Model):
    current = models.BooleanField(default=False)
    drill = models.ForeignKey(Drill)
    number = models.IntegerField()

    def __unicode__(self):
        return str(self.number)
    
    def set_current(self, set_id):
        #Set.objects.get(current=True).current=False
        #Set.objects.get(id=set_id).current=True
        
        return 

class StudentLoc(models.Model):
    set = models.ForeignKey(Set)
    s_id = models.IntegerField()
    rel_x = models.IntegerField()
    rel_y = models.IntegerField()
    #saved_lat = models.DecimalField()??

    def __unicode__(self):
        return "Set="+str(set)+" s_id="+str(self.s_id)+" rel_x="+str(self.rel_x)+ "rel_y="+str(self.rel_y)
