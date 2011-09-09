Django Snippets Cream
=====================

Django app packaging the best snippets found on http://djangosnippets.org


Included Snippets
-----------------

186. Profiling Middleware
+++++++++++++++++++++++++
Displays hotshot profiling for any view. Add a "prof" key to the query string by appending ?prof (or &prof=) and you'll see the profiling results in your browser, i.e. http://yoursite.com/yourview/?prof

Original Snippet - http://djangosnippets.org/snippets/186/

To enable add ``snippetscream.ProfileMiddleware`` to your ``MIDDLEWARE_CLASSES`` setting, i.e.::
    
    MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('snippetscream.ProfileMiddleware',)

963. RequestFactory 
++++++++++++++++++++
Easily create mock request objects for use in testing.

Original Snippet - http://djangosnippets.org/snippets/963/

Example::

    from snippetscream import RequestFactory
    request = RequestFactory().get('/')

1031. Model Inheritance With Content Type 
+++++++++++++++++++++++++++++++++++++++++
Supplies a model class aware of its child models, allowing for child class objects to be resolved from parent objects.

Original Snippet - http://djangosnippets.org/snippets/1031/

Example::

    === example usage in interpreter ===
    >>> from snippetscream import PolyModel
    >>> class TrunkModel(PolyModel):
    ...     pass
    >>> class LeafModel(TrunkModel):
    ...     pass
    >>> leaf_obj = LeafModel()
    >>> leaf_obj.save()
    >>> trunk_obj = TrunkModel.objects.get(id=leaf_obj.id)
    >>> trunk_obj
    ... <TrunkModel: TrunkModel object>
    >>> trunk_obj.as_leaf_class()
    ... <LeafModel: LeafModel object>
    

1378. Resolve URLs to View Name
+++++++++++++++++++++++++++++++
Supplies a resolve_to_name function that takes in a path and resolves it to a view name or view function name (given that the path is actually defined in your urlconf).

Original Snippet - http://djangosnippets.org/snippets/1378/

Example::

    === urlconf ====
    urlpatterns = patterns(''
        url(r'^some/url/$', 'app.views.view'),
        url(r'^some/other/url/$', 'app.views.other.view', name='this_is_a_named_view'),
    )

    === example usage in interpreter ===
    >>> from snippetscream import resolve_to_name
    >>> print resolve_to_name('/some/url/')
    'app.views.view'
    >>> print resolve_to_name('/some/other/url/')
    'this_is_a_named_view'

1875. Auto-create Django Admin User During syncdb
+++++++++++++++++++++++++++++++++++++++++++++++++
This avoids the frustrating step of having to set up a new admin user every time you re-initialize your database. 

Original Snippet - http://djangosnippets.org/snippets/1875/

To enable add ``snippetscream`` to your ``INSTALLED_APPS`` settings and create the following setting::

    CREATE_DEFAULT_SUPERUSER = True

2240. CSV Serializer
++++++++++++++++++++
Supplies CSV serialization for models. Can be used via the ``dumpdata/loaddata`` management commands or programmatically using the ``django.core.serializers`` module. Supports multiple header lines and natural keys.

Original Snippet - http://djangosnippets.org/snippets/2240/

To enable add ``snippetscream.csv_serializer`` to your ``SERIALIZATION_MODULES`` setting, i.e.::
    
    SERIALIZATION_MODULES = {
        'csv': 'snippetscream.csv_serializer',
    }

Example::

    === example dumpdata usage ===
    $ python manage.py dumpdata --format csv auth.user > users.csv

    === example usage in interpreter ===
    >>> from django.core import serializers
    >>> csvdata = serializers.serialize('csv', Foo.objects.all())

2536. Configurable defaults for contrib.sites default Site during syncdb
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Modelled after #1875, this provides a more sensible default for the ``Site``
object created during the first pass of ``syncdb`` (default domain of
``localhost:8000``). It means that the admin's *view on site* button will work
automagically, amongst other things.

Original Snippet - http://djangosnippets.org/snippets/2536/

To enable add ``snippetscream`` to your ``INSTALLED_APPS`` settings and create the following setting::

    CREATE_DEFAULT_SITE = True

If you'd like to customise the default ``Site`` yourself, you can specify ``DEFAULT_SITE_DOMAIN`` and ``DEFAULT_SITE_NAME`` settings, e.g::
    
    DEFAULT_SITE_DOMAIN = 'my.site.com'
    DEFAULT_SITE_NAME = 'My Site'

Optionally you can manually call the ``create_default_site`` method and pass ``name`` and ``domain`` arguments which take precedence over the settings parameters.

