Django Snippets Cream
=====================

Django app packaging the best snippets found on http://djangosnippets.org


Included Snippets
-----------------

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

