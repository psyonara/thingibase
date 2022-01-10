from django.db import models


class Thing(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    updated_at = models.DateTimeField(null=True)
    thingiverse_id = models.IntegerField(null=False)


class Image(models.Model):
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
    source_url = models.URLField(null=False)


class File(models.Model):
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
    source_url = models.URLField(null=False)
