from django.shortcuts import render, redirect
from .form import ImageForm
from .models import Image

# Create your views here.


def index(request):
    if request.method == "POST":
        form = ImageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            obj = form.instance
            print(obj)
            return render(request, "index.html", {"obj": obj, "form": ImageForm()})
    else:
        form = ImageForm()
        img = Image.objects.all()
    return render(request, "index.html", {"form": form})