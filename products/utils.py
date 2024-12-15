from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

def author_required(model, lookup_field="pk"):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            obj = get_object_or_404(model, **{lookup_field: kwargs[lookup_field]})
            if obj.author != request.user:
                return HttpResponseForbidden("작성자만 수정/삭제 가능")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
