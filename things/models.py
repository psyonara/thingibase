from django.db import models


class Thing(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    updated_at = models.DateTimeField(null=True)
    thingiverse_id = models.IntegerField(null=False)
