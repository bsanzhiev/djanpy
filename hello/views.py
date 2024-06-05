from datetime import date
import re
from django.utils.timezone import datetime
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.generic import ListView

from hello.forms import LogMessageForm
from hello.models import LogMessage

def hello_there(request, name):
  # Filter the name argument to letters only using regular expressions. URL arguments
  # can contain arbitrary text, so we restrict to safe characters only.
  print(request.build_absolute_uri())
  return render(
    request,
    'hello/hello_there.html',
    {
      'name': name,
      'date': datetime.now()
    }
  )
  
class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

def about(request):
  return render(request, "hello/about.html")

def contact(request):
  return render(request, "hello/contact.html")

def log_message(request):
  form = LogMessageForm(request.POST or None)
  
  if request.method == "POST":
    if form.is_valid():
      message = form.save(commit=False)
      message.log_date = datetime.now()
      message.save()
      return redirect("home")
    else:
      form = LogMessageForm()
  
  return render(request, "hello/log_message.html", {"form": form})
