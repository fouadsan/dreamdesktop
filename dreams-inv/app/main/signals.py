from django.db.models.signals import post_save
from .models import Product
from django.dispatch import receiver
from .models import Barcode


@receiver(post_save, sender=Product)
def create_barcode(sender, instance, created, **kwargs):
    if created:
        Barcode.objects.create(product=instance)


@receiver(post_save, sender=Product)
def save_barcode(sender, instance, **kwargs):
    instance.barcode.save()
