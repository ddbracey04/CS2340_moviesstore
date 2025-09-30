from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Petition(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    vote = models.IntegerField(blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='petition_images/', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # # voterIds = VoterList()
    # ownerId = models.IntegerField(blank=True, null=True)
    # voters = models.ManyToManyField(Voter)
    def __str__(self):
        return str(self.id) + ' - ' + self.name

class VoteBallot(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.IntegerField()
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id)
