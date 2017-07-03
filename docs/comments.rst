Comments
========

You can add comments to any kind of object. The easy integration that comes with the app expects a `ViewSet <http://www.django-rest-framework.org/api-guide/viewsets/>`_ of the respective model.


Adding comments to a model
--------------------------

Import the CommentsMixin in your ``views.py``::

    from ..comments.mixins import CommentsMixin

Add the CommentsMixin to your ViewSet like in this example::

    class MyViewSet(CommentsMixin, viewsets.ModelViewSet):
        ...


Setting up the endpoint
-----------------------

.. note:: If you use a router from the Django REST Framework you don't need to add anything. There will be an additional endpoint ``/comments/`` under the url of your ViewSet.

Otherwise add the endpoint to your ``urlpatterns`` in ``urls.py`` somehow like this::

    url(
        r'^mymodel/(?P<pk>[\w.@+-]+)/comments/$',
        MyViewSet.as_view({'get': 'comments', 'post': 'comments'})
    ),


Posting a comment
-----------------

Any logged in user can now post a comment by sending a POST to the respective endpoint. It should have a json like this::

    {"content": "This is a comment."}


Getting posted comments
-----------------------

Any logged in user can get the posted comments by sending a GET to the respective endpoint.
