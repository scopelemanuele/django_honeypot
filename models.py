# -*- coding: utf-8 -*-
#python3 compatibility
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext, ugettext_lazy as _

# Create your models here.
from datetime import timedelta, datetime, date


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
    . fields.
    updating ``created`` and ``modified``
    """
    created = models.DateTimeField(editable=True, auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class HoneypotLog(TimeStampedModel):
    ip = models.IPAddressField()
    last_activity = models.IntegerField(default=255)
    rating = models.IntegerField(default=0)
    from_url = models.CharField(max_length=1024, default=None, null=True)
    request_url = models.CharField(max_length=1024, default=None, null=True)
    type = models.CharField(max_length=255)

    class Meta:
        verbose_name = _('HoneyPot')
        verbose_name_plural = _('HoneyPots')
        ordering = ['created']


class LogOptions(admin.ModelAdmin):
    list_display = ('ip', 'last_activity', 'rating', 'type', 'request_url', 'created')
    list_filter = ['created', 'type']


admin.site.register(HoneypotLog, LogOptions)
