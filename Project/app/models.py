from django.db import models
from django.contrib.auth.models import User,AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True)
    
    avatar = models.ImageField(null=True,default='avatar.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# If we have Topic class somewhere below the Room class, so we know that there will be import issues.
# Fix: name of the foreignkey class in quotes.
# topic = models.ForeignKey('Topic', on_delete=models.SET_NULL, null=True)

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)

    participants = models.ManyToManyField(User, related_name='participants')
    
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    updated = models.DateTimeField(auto_now=True) # Time will be changed on update
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-updated','-created']

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.body[0:50] 