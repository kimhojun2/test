from django.db import models

# Create your models here.
class location(models.Model):
    loca_file = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_quiz = models.BooleanField(default=False)


class route(models.Model):
    pass