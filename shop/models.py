from django.db import models


class Feature(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    subtitle = models.TextField()
    backdrop = models.ImageField(upload_to='features/%Y/%m/%d', blank=True)

    def __str__(self):
        return self.title
