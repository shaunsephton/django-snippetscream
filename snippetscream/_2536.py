# -*- coding: utf-8 -*-
"""
Configurable defaults for ``django.contrib.sites`` default
``Site`` during syncdb

Modelled after snippet #1875, this provides a more sensible default
for the ``Site`` object created during the first pass of syncdb
(default domain of localhost:8000). It means that the admin's view on
site button will work automagically, amongst other things.

Original: http://djangosnippets.org/snippets/2536/

"""
from django.conf import settings


# Configure default Site creation with better defaults, and provide
# overrides for those defaults via settings and kwargs:
def create_default_site(app, created_models, verbosity, db, **kwargs):
    from django.contrib.sites.models import Site

    name, domain = kwargs.pop('name', None), kwargs.pop('domain', None)

    if not name:
        name = getattr(settings, 'DEFAULT_SITE_NAME', 'example.com')
    if not domain:
        domain = getattr(settings, 'DEFAULT_SITE_DOMAIN', 'localhost:8000')

    if Site in created_models:
        obj = Site(domain=domain, name=name)
        if verbosity >= 2:
            print('Creating default Site object:\nname: %s\ndomain: %s' % (
                name, domain))
        obj.save(using=db)

    Site.objects.clear_cache()


if getattr(settings, 'CREATE_DEFAULT_SITE', False):
    from django.db.models import signals
    from django.contrib.sites import models as sites_app
    from django.contrib.sites import management as original

    # Disconnect original site creator.
    signals.post_syncdb.disconnect(
        original.create_default_site,
        sender=sites_app,
    )

    # Trigger default site creation.
    signals.post_syncdb.connect(
        create_default_site,
        sender=sites_app,
        dispatch_uid='snippetscream._2536.create_default_site'
    )
