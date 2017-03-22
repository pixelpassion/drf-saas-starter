import json
from io import BytesIO

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.template.loader import render_to_string
from django.shortcuts import render
from django.http import HttpResponse

from weasyprint import HTML, CSS

TEMPLATES_PREFIX = "htmltopdf/"

class CustomPDF(models.Model):

    template = models.CharField(
        _("Name of template"),
        help_text=_("Name of template file without file extension"),
        null=False,
        blank=False
    )

    context = JSONField(
        _("Context for filling in template"),
        help_text=_(""),
        null=False,
        blank=False
    )

    output_filename = models.CharField(
        _("Name of output PDF file"),
        help_text=_(),
        null=False,
        blank=False
    )

    def make_output(self, request):
        """Returns HttpResponse containing pdf output
       
        Views calling this method must pass the request as well.
        """

        rendered_html = render_to_string("{}{}.html".format(TEMPLATE_PREFIX, self.template), self.context, request)
        
        buf = BytesIO()

        HTML(
            string=rendered_html,
            base_url=request.build_absolute_uri()
        ).write_pdf(buf)

        buf.seek(0)
        pdf_output = buf.read()
        buf.close()

        response = HttpResponse(pdf_output, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="{}"'.format(self.output_filename)

        return response
