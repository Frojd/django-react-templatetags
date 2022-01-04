from __future__ import unicode_literals

from django.db import models

from django_react_templatetags.mixins import RepresentationMixin


class Person(RepresentationMixin, models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def to_react_representation(self, context={}):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
        }


class Movie(RepresentationMixin, models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField()

    def to_react_representation(self, context={}):
        return {
            "title": self.title,
            "year": self.year,
            "current_path": context["request"].path,
        }


class MovieWithContext(RepresentationMixin, models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField()

    def to_react_representation(self, context={}):
        return {
            "title": self.title,
            "year": self.year,
            "search_term": context["search_term"],
        }
