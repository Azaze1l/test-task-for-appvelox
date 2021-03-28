import functools
import traceback
from django.http.response import JsonResponse
from tasks_api.settings import DEBUG

JSON_DUMPS_PARAMS = {
    'ensure_ascii': False
}


def _error_response(exception):
    if DEBUG:
        response = {"message": str(exception), "traceback": traceback.format_exc()}
    else:
        response = {"message": str(exception)}
    return JsonResponse(response, status=500, json_dumps_params=JSON_DUMPS_PARAMS)


def protected_view(function):
    """
    Декоратор для отлова серверных ошибок
    """
    @functools.wraps(function)
    def inner(request, *args, **kwargs):
        try:
            return function(request, *args, **kwargs)
        except Exception as e:
            return _error_response(e)
    return inner
