# http://djangosnippets.org/snippets/1031/

from django.contrib.contenttypes.models import ContentType
from django.db import models


class PolyModel(models.Model):
    """
    Model class aware of its child models, allowing for child class objects
    to be resolved from parent objects.

    For example:
    Contact is a parent class inheriting from PolyModel. Subclasses might be
    Company, Person, Artist, Label etc. Basic address, email etc. fields can
    be added to the parent class and all subclasses will have those.

    Having searched your database for Contact objects (undifferentiated by
    class) you then want to reload the chosen object as the subclass
    that it really is:

    thing.as_leaf_class()
    """
    content_type = models.ForeignKey(
        ContentType,
        editable=False,
        null=True
    )
    class_name = models.CharField(
        max_length=32,
        editable=False,
        null=True
    )

    class Meta:
        abstract = True

    def as_leaf_class(self):
        """
        Returns the leaf class no matter where the calling instance
        is in the inheritance hierarchy.
        """
        try:
            return self.__getattribute__(self.class_name.lower())
        except AttributeError:
            content_type = self.content_type
            model = content_type.model_class()
            if(PolyModel in model.__bases__):
                return self
            return model.objects.get(id=self.id)

    def save(self, *args, **kwargs):
        """
        Save field required for leaf class resolution.
        """
        # set leaf class content type
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.\
                    __class__)

        # set leaf class class name
        if not self.class_name:
            self.class_name = self.__class__.__name__

        super(PolyModel, self).save(*args, **kwargs)
