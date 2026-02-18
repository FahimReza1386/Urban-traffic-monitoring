# Third-Party
from rest_framework.renderers import JSONRenderer


class CustomJsonRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response") if renderer_context else None

        if response and response.status_code >= 400:
            formatted_data = {
                "msg": "Request Failed",
                "code": response.status_code,
                "data": data,
            }
        else:
            formatted_data = {
                "msg": "Request Success",
                "code": response.status_code if response else 200,
                "data": data,
            }

        return super().render(formatted_data, accepted_media_type, renderer_context)
