# http://djangosnippets.org/snippets/1875/

from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.auth.management import create_superuser
from django.db.models import signals


def create_default_superuser(app, created_models, verbosity, **kwargs):
    """
    Creates our default superuser.
    """
    try:
        auth_models.User.objects.get(username='admin')
    except auth_models.User.DoesNotExist:
        print 'Creating default superuser:\nUsername: admin\nPassword: \
admin\nEmail: invalid@ddress.com'
        assert auth_models.User.objects.create_superuser('admin', \
                'invalid@ddress.com', 'admin')
    else:
        print 'Default superuser already exists.'

if getattr(settings, 'CREATE_DEFAULT_SUPERUSER', False):
    # From http://stackoverflow.com/questions/1466827/:
    # Prevent interactive question about wanting a superuser created.
    # (This code has to go in this otherwise empty "models" module
    # so that it gets processed by the "syncdb" command during
    # database creation.)
    signals.post_syncdb.disconnect(
        create_superuser,
        sender=auth_models,
        dispatch_uid='django.contrib.auth.management.create_superuser'
    )

    # Trigger default superuser creation.
    signals.post_syncdb.connect(
        create_default_superuser,
        sender=auth_models,
        dispatch_uid='common.models.create_testuser'
    )
