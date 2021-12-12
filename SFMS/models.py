from django.db import models

# Create your models here.
class students(models.Model):
    name = models.CharField(max_length=225)
    # last_name = models.Charfield(max_length=225)
    # created_on = models.DateTimeField(auto_now_add=True)
    # modified_on = models.DateTimeField(auto_now=True)
    # login_count = models.PositiveIntegerField(default=0)
    # gender = models.CharField(max_length=1, choices=GENDER_TYPES)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.name

