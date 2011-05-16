from django.db import models


class Food (models.Model):
    """Something edible.
    """
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class Unit (models.Model):
    """A form of measurement.
    """
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


