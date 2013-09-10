from django.db import models

# Create your models here.
class SignUp(models.Model):
    ''' Represents an interested user! '''
    email = models.EmailField()

    def __unicode__(self):
        return self.email
