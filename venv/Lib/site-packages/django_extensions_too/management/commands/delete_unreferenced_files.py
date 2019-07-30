# -*- coding: utf-8 -*-

# Copyright 2016
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tims@thegoco.com>
#
# Inspired by: https://github.com/django-extensions/django-extensions/blob/master/django_extensions/management/commands/unreferenced_files.py

# -----------------------------------------------------------------------------

import os
from collections import defaultdict

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import models

from django_extensions.management.utils import signalcommand

from django_extensions_too.management.color import color_style

# -----------------------------------------------------------------------------


class Command(BaseCommand):
    help = "Deletes all files in MEDIA_ROOT that are not referenced in the database."

    @signalcommand
    def handle(self, *args, **options):
        self.style = color_style()

        if settings.MEDIA_ROOT == '':
            print(self.style.WARN('MEDIA_ROOT is not set, nothing to do'))
            return

        # Get a list of all files under MEDIA_ROOT
        media = set()
        for root, dirs, files in os.walk(settings.MEDIA_ROOT):
            for f in files:
                media.add(os.path.abspath(os.path.join(root, f)))

        # Get list of all fields (value) for each model (key)
        # that is a FileField or subclass of a FileField
        model_dict = defaultdict(list)
        for model in apps.get_models():
            for field in model._meta.fields:
                if issubclass(field.__class__, models.FileField):
                    model_dict[model].append(field)

        # Get a list of all files referenced in the database
        referenced = set()
        for model in model_dict:
            all = model.objects.all().iterator()
            for object in all:
                for field in model_dict[model]:
                    target_file = getattr(object, field.name)
                    if target_file:
                        referenced.add(os.path.abspath(target_file.path))

        # Print each file in MEDIA_ROOT that is not referenced in the database
        not_referenced = media - referenced
        for f in not_referenced:
            print(f)
            os.remove(f)
