actstream-drf
=============

This app provides an integration of `Django Activity Stream <http://django-activity-stream.readthedocs.io/en/latest/index.html>`_ with the Django REST Framework.


Creating actions
----------------

Import action from actstream::

    from actstream import action

If you would call it from the save method of a Comment model it could look like this::

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        action.send(self.author, verb='made comment', action_object=self, target=self.content_object)

For more information on the usage of Django Activity Stream please read the documentation: http://django-activity-stream.readthedocs.io/en/latest/index.html


Adding serializers to actstream_drf
-----------------------------------

In order to access the information that you have created by the action, you need to define serializers for the models involved.

.. warning:: Think about what serializer to use. Which fields should be serialized and transmitted?

In ``serializers.py`` of actstream_drf change and add serializers to the to_representation method of ActionObjectGenericRelatedField.


Accessing activities that correspond to a model
-----------------------------------------------

Import the ActivitiesMixin in your ``views.py``::

    from ..actstream_drf.mixins import ActivitiesMixin

Add the ActivitiesMixin to your ViewSet like in this example::

    class MyViewSet(ActivitiesMixin, viewsets.ModelViewSet):
        ...


Setting up the endpoint
-----------------------

.. note:: If you use a router from the Django REST Framework you don't need to add anything. There will be an additional endpoint ``/activities/`` under the url of your ViewSet.

Otherwise add the endpoint to your ``urlpatterns`` in ``urls.py`` somehow like this::

    url(
        r'^mymodel/(?P<pk>[\w.@+-]+)/activities/$',
        MyViewSet.as_view({'get': 'activities'})
    ),


Getting activities
------------------

Any logged in user can get the activities by sending a GET to the respective endpoint.
