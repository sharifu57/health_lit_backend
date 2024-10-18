from django.db import models
import pendulum
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class BaseModel(models.Model):
    is_active = models.BooleanField(default=True, null=True, blank=True)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    
    def softDelete(self):
        self.is_deleted = True
        self.is_active = False
        self.updated_at = pendulum.now()
        self.save()
        

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="profile")
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        
        return f"{self.user.username} - {self.phone_number}"
    
    
    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()
    
