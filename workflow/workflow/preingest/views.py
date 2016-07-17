from django.http import HttpResponse

from tasks import Sleepy

def index(request):
    task = Sleepy().delay("bar")
    return HttpResponse("<h1>Preingest</h1>")
