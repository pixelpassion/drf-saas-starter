from django.views.generic import View

from .models import CustomPDF

EXAMPLE_TEMPLATE = "example"
EXAMPLE_CONTEXT = {'name': 'cheryl'}
EXAMPLE_OUTPUT_NAME = "example_output.pdf"

class ExamplePDF(View):

    def get(self, request):
        example_pdf = CustomPDF(
            template=EXAMPLE_TEMPLATE,
            context=EXAMPLE_CONTEXT,
            output_filename=EXAMPLE_OUTPUT_NAME
        )

        return example_pdf.make_output(request)

example = ExamplePDF.as_view()
