from rest_framework.response import Response
from rest_framework import status
from rest_framework import renderers
import json

class CustomRenderer(renderers.BaseRenderer):
    charset = 'utf-8'
    media_type = 'application/json'
    format = 'json'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors': data})
        else:
            response = json.dumps(data)
        return response