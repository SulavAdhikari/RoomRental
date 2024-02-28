from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_info = models.CharField(max_length=255)

    def __str__(self):
        return str(self.user.username + " Profile.")

class Room(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rent = models.DecimalField(max_digits=8, decimal_places=2)
    location = models.CharField(max_length=255)
    photos = models.ImageField(upload_to='room_photos/', null=True, blank=True)
    bhk = models.IntegerField()
    bathroom = models.IntegerField()

    def __str__(self):
        return str(self.owner.user.username + " - " + self.location)


class Application(models.Model):
    applicant = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.applicant.user.username + " - " + self.room.location)