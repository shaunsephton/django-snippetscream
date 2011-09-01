import sys
import tempfile
import hotshot
from django.conf import settings
from cStringIO import StringIO

# Don't fail if profile module not found. Not ideal, but we don't want
# all snippets to be unavailable due to one misbehaving.
try:
    import profile
except ImportError, e:
    pass
else:
    import hotshot.stats


class ProfileMiddleware(object):
    """
    Displays hotshot profiling for any view.
    http://yoursite.com/yourview/?prof

    Add the "prof" key to query string by appending ?prof (or &prof=)
    and you'll see the profiling results in your browser.
    It's set up to only be available in django's debug mode,
    but you really shouldn't add this middleware to any production
    configuration.
    * Only tested on Linux
    """
    def process_request(self, request):
        if settings.DEBUG and ('prof' in request.GET):
            self.tmpfile = tempfile.NamedTemporaryFile()
            self.prof = hotshot.Profile(self.tmpfile.name)

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if settings.DEBUG and ('prof' in request.GET):
            return self.prof.runcall(callback, request, *callback_args, \
                    **callback_kwargs)

    def process_response(self, request, response):
        if settings.DEBUG and ('prof' in request.GET):
            self.prof.close()

            out = StringIO()
            old_stdout = sys.stdout
            sys.stdout = out

            stats = hotshot.stats.load(self.tmpfile.name)
            #stats.strip_dirs()

            stats.sort_stats('time', 'calls')
            stats.print_stats()

            sys.stdout = old_stdout
            stats_str = out.getvalue()

            if response and response.content and stats_str:
                response.content = "<pre>" + stats_str + "</pre>"

            response['Content-Type'] = 'text/html'
        return response
