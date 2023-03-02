import json
import logging

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        log_data = {
            "method": request.method,
            "path": request.path,
            "query_params": dict(request.GET),
            "data": request.body.decode("utf-8"),
            "remote_addr": request.META.get("REMOTE_ADDR", ""),
            "user_agent": request.META.get("HTTP_USER_AGENT", ""),
        }
        logger.debug(json.dumps(log_data))

        response = self.get_response(request)
        return response