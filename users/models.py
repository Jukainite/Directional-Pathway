from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)



class finger_image(models.Model):  
    caption = models.CharField(max_length=200)  
    # image = models.ImageField(upload_to='images')  
    image = models.ImageField(upload_to='finger_images')
    def __str__(self):  
        return self.caption  
    
class face_image(models.Model):  
    caption = models.CharField(max_length=200)  
    # image = models.ImageField(upload_to='images')  
    image = models.ImageField(upload_to='face_images')
    def __str__(self):  
        return self.caption  
    
class qr_image(models.Model):  
    bill = models.CharField(max_length=200, primary_key=True)  
    # image = models.ImageField(upload_to='images')  
    image = models.ImageField(upload_to='QR_images')
    def __str__(self):  
        return self.caption  
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    def __str__(self):
        return f'{self.user.username} - {self.stars}' 