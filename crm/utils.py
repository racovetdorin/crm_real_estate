try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

# Thread local storage is a way to store data that only the current thread can
# access. In a multi-threaded server environment, each request gets dispatched
# to a thread, which then returns a response.
#
# The purpose of the local storage is to provide context during the lifecycle
# of a request which is then cleared.as
#
# E.g.  Limit the database working set to models belonging to a specific
# agency
_thread_locals = local()


def set_office(office):
    """
    Set the agency for this request-response cycle.
    """
    _thread_locals.office = office


def get_office():
    """
    Return the currently active agency.
    """
    return getattr(_thread_locals, 'office', None)


def set_request(request):
    """
    Save the request in TLS.
    """
    _thread_locals.request = request


def get_request():
    """
    Return the currently active request.
    """
    return getattr(_thread_locals, 'request', None)


def get_user():
    """
    Return the currently logged in user.
    """
    return get_request().user
