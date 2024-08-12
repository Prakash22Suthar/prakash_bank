from rest_framework.renderers import JSONRenderer 
from rest_framework import status

def get_status(code):
    for name, val in status.__dict__.items():
        if not callable(val) and code is val:
            return name.replace(f"HTTP_{code}_","")
    return "UNKNOWN"

class CustomRenderer(JSONRenderer):

    """ Custom Renderer to get custome response for API's """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context["response"]
        modified_response = {}
        modified_response["code"]=response.status_code
        modified_response["status"]=get_status(response.status_code)
        if status.is_client_error(response.status_code) or status.is_server_error(response.status_code):
            modified_response["error"] = data
        else:
            modified_response["data"] = data
        return super().render(modified_response, accepted_media_type, renderer_context)
