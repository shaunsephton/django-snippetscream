Django Snippets Cream
=====================

Django app packaging the best snippets found on http://djangosnippets.org


Included Snippets
-----------------

186. Profiling Middleware
+++++++++++++++++++++++++
Displays hotshot profiling for any view. Add a "prof" key to the query string by appending ?prof (or &prof=) and you'll see the profiling results in your browser, i.e. http://yoursite.com/yourview/?prof

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
        (r'/some/url', 'app.views.view'),
        (r'/some/other/url', 'app.views.other.view', {}, 'this_is_a_named_view'),
    )

    === example usage in interpreter ===
    >>> from snippetscream import resolve_to_name
    >>> print resolve_to_name('/some/url')
    'app.views.view'
    >>> print resolve_to_name('/some/other/url')
    'this_is_a_named_view'

1875. Auto-create Django Admin User During syncdb
+++++++++++++++++++++++++++++++++++++++++++++++++
This avoids the frustrating step of having to set up a new admin user every time you re-initialize your database. 

Original Snippet - http://djangosnippets.org/snippets/1875/

To enable add ``snippetscream`` to your ``INSTALLED_APPS`` settings and create the following setting::

    CREATE_DEFAULT_SUPERUSER = True

