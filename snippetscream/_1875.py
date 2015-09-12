# -*- coding: utf-8 -*-
"""
Auto-create Django admin user during syncdb

This avoids the frustrating step of having to set up a new admin user
every time you re-initialize your database.

Adapted from http://stackoverflow.com/questions/1466827/

Original: http://djangosnippets.org/snippets/1875/

"""

import importlib
from django.conf import settings

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

    
def create_default_superuser(app, created_models, verbosity, **kwargs):
    try:
        User.objects.get(username='admin')
    except User.DoesNotExist:
        if verbosity >= 2:
            print("Creating default superuser:\nusername: %s\npassword: %s\nemail: %s" % (
                "admin", "admin", "invalid@address.com"))
        assert User.objects.create_superuser(
            username='admin', email='invalid@address.com', password='admin')


if getattr(settings, 'CREATE_DEFAULT_SUPERUSER', False):
    from django.db.models import signals
    from django.contrib.auth.management import create_superuser

    signals.post_syncdb.disconnect(
        create_superuser,
        sender=importlib.import_module(User.__module__),
    )

    # Trigger default superuser creation.
    signals.post_syncdb.connect(
        create_default_superuser,
        sender=importlib.import_module(User.__module__),
        dispatch_uid='snippetscream._1875.create_default_superuser'
    )
