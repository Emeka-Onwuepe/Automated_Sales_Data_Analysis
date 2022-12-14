from django.db import models
from users.models import User_id

# Create your models here.

class Dataset(models.Model):
    """Model definition for Dataset."""

    # TODO: Define fields here
    user_id  = models.ForeignKey(User_id, on_delete=models.CASCADE,related_name="dataset_user_id")
    dataset_id = models.CharField("dataset_id",max_length = 150,blank=None)
    dataset = models.FileField("dataset",blank=False)
    report_title = models.CharField("report title",blank=False,max_length = 256) 
    currency_symbol = models.CharField("currency symbol",blank=False,max_length = 10) 
    zipfolder = models.FileField("zipfolder",blank=True)
    columns = models.TextField("columns",blank=True)
    created = models.DateTimeField("created",auto_now_add = True)
    
    class Meta:
        """Meta definition for Dataset."""

        verbose_name = 'Dataset'
        verbose_name_plural = 'Datasets'

    def __str__(self):
        """Unicode representation of Dataset."""
        return f'{self.dataset_id} {self.dataset}'


    # TODO: Define custom methods here
