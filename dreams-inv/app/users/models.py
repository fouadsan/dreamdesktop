from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField(null=False, blank=False)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        try:
            this = Profile.objects.get(id=self.id)
            if this.image != self.image and this.image != 'default.jpg':
                this.image.delete()
        except: pass
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if (img.height > 300) or (img.width > 300):
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)





