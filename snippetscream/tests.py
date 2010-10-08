import unittest

from django.contrib.contenttypes.models import ContentType

from snippetscream import PolyModel

class PolyTrunkModel(PolyModel):
    pass
models.register_models('panya', TrunkModel)
class PolyBranchModel(PolyTrunkModel):
    pass
models.register_models('panya', BranchModel)
class PolyLeafModel(PolyBranchModel):
    pass
models.register_models('panya', LeafModel)

class PolyModel(unittest.TestCase):
    def test_save(self):
        # leaf class content type should be set on save
        obj = PolyLeafModel(title='title')
        obj.save()
        self.failUnless(obj.content_type == ContentType.objects.get_for_model(PolyLeafModel))
        
        # leaf class class name should be set on save
        self.failUnless(obj.class_name == PolyLeafModel.__name__)

        # correct leaf class content type should be retained over base class' content type
        base = obj.modelbase_ptr
        base.save()
        self.failUnless(base.content_type == ContentType.objects.get_for_model(PolyLeafModel))
       
        # correct leaf class class name should be retained over base class' class name
        self.failUnless(base.class_name == PolyLeafModel.__name__)

    def test_as_leaf_class(self):
        obj = PolyLeafModel(title='title')
        obj.save()

        # always return the leaf class, no matter where we are in the hierarchy
        self.failUnless(PolyTrunkModel.objects.get(slug=obj.slug).as_leaf_class() == obj)
        self.failUnless(PolyBranchModel.objects.get(slug=obj.slug).as_leaf_class() == obj)
        self.failUnless(PolyLeafModel.objects.get(slug=obj.slug).as_leaf_class() == obj)
