from rest_framework import exceptions
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers


def get_swagger_view(title=None, url=None):
    """Return schema view which renders Swagger/OpenAPI. (Replace with DRF get_schema_view shortcut in 3.5)

    Args:
      title: (Default value = None)
      url: (Default value = None)

    Returns:

    """
    class SwaggerSchemaView(APIView):
        """ """
        _ignore_model_permissions = True
        exclude_from_schema = True
        authentication_classes = [SessionAuthentication, ]
        permission_classes = [AllowAny, ]
        renderer_classes = [
            CoreJSONRenderer,
            renderers.OpenAPIRenderer,
            renderers.SwaggerUIRenderer
        ]

        def get(self, request):
            """

            Args:
              request:

            Returns:

            """
            generator = SchemaGenerator(title=title, url=url)
            schema = generator.get_schema(request=request)

            if not schema:
                raise exceptions.ValidationError(
                    'The schema generator did not return a schema Document'
                )

            return Response(schema)

    return SwaggerSchemaView.as_view()
