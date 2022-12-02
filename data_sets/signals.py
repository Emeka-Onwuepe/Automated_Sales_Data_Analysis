from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import Dataset

@receiver(pre_save, sender=Dataset)
def delete_dataset_file(sender, instance, *args, **kwargs):
 
    if instance.pk:
        dataset = Dataset.objects.get(pk=instance.pk)

        if dataset.dataset != instance.dataset:
           dataset.dataset.delete(False)
            
        if dataset.zipfolder and instance.zipfolder:
            dataset.zipfolder.delete(False)


@receiver(post_delete, sender=Dataset)
def delete_dataset_files(sender, instance, using, *args, **kwargs):
    if instance.pk:
        instance.zipfolder.delete(save=False)
        instance.dataset.delete(False)
        
