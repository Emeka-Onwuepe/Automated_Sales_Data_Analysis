from django.db import models

# Create your models here.
class User_id(models.Model):
    """Model definition for user_id."""
     
    user_id  = models.CharField("user_id",max_length = 150,blank=None)
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for user_id."""

        verbose_name = 'user_id'
        verbose_name_plural = 'user_ids'

    def __str__(self):
        """Unicode representation of user_id."""
        return self.user_id

    # TODO: Define custom methods here
