import unittest

from django.contrib.contenttypes.models import ContentType

from snippetscream import PolyModel

class PolyTrunkModel(PolyModel):
    pass
class PolyBranchModel(PolyTrunkModel):
    pass
class PolyLeafModel(PolyBranchModel):
    pass

class PolyModel(unittest.TestCase):
    def test_save(self):
        # Leaf class content type should be set on save.
        obj = PolyLeafModel()
        obj.save()
        self.failUnless(obj.content_type == ContentType.objects.get_for_model(PolyLeafModel))
        
        # Leaf class class name should be set on save.
        self.failUnless(obj.class_name == PolyLeafModel.__name__)

        # Correct leaf class content type should be retained over base class' content type.
        base = obj.polytrunkmodel_ptr
        base.save()
        self.failUnless(base.content_type == ContentType.objects.get_for_model(PolyLeafModel))
       
        # Correct leaf class class name should be retained over base class' class name.
        self.failUnless(base.class_name == PolyLeafModel.__name__)

    def test_as_leaf_class(self):
        obj = PolyLeafModel()
        obj.save()

        # Always return the leaf class, no matter where we are in the hierarchy.
        self.failUnless(PolyTrunkModel.objects.get(id=obj.id).as_leaf_class() == obj)
        self.failUnless(PolyBranchModel.objects.get(id=obj.id).as_leaf_class() == obj)
        self.failUnless(PolyLeafModel.objects.get(id=obj.id).as_leaf_class() == obj)

        # Trunk only object should traverse to itself.
        trunk_obj=PolyTrunkModel()
        trunk_obj.save()
        self.failUnless(PolyTrunkModel.objects.get(id=trunk_obj.id).as_leaf_class() == trunk_obj)
