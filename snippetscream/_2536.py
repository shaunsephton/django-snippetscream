#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Adapted From Http://stackoverflow.com/questions/1466827/ --
from django.conf import settings
from django.db.models import signals
from django.contrib.sites.models import Site
from django.contrib.sites import models as site_app
from django.contrib.sites.management import create_default_site as orig_default_site


# Configure default Site creation with better defaults, and provide
# overrides for those defaults via settings and kwargs:
def create_default_site(app, created_models, verbosity, db, **kwargs):
    name  = kwargs.pop('name', None)
    domain = kwargs.pop('domain', None)

    if not name:
        name = getattr(settings, 'DEFAULT_SITE_NAME', 'example.com')
    if not domain:
        domain = getattr(settings, 'DEFAULT_SITE_DOMAIN', 'localhost:8000')

    if Site in created_models:
        if verbosity >= 2:
            print 'Creating default Site object:\nname: %s\ndomain: %s' % (name, domain)
        s = Site(domain=domain, name=name)
        s.save(using=db)
    Site.objects.clear_cache()

if getattr(settings, 'CREATE_DEFAULT_SITE', False):
    # Disconnect original site creator.
    signals.post_syncdb.disconnect(
        orig_default_site,
        sender=site_app,
    )

    # Trigger default site creation.
    signals.post_syncdb.connect(
        create_default_site,
        sender=site_app,
        dispatch_uid='snippetscream._2536.create_default_site'
    )
