from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate


from .models import Todolist, Item
from .forms import CreateNewList
# Create your views here.

def index(response, id):
    """
    It takes the id of a todolist, checks if the user has access to it, and if so, 
    it renders the list.html template with the todolist as the context
    
    :param response: The response object that is passed to the view
    :param id: the id of the list
    :return: The response object is being returned.
    """
    ls = Todolist.objects.get(id = id)

    if ls in response.user.todolist.all():

        if response.method == "POST":
            print(response.POST)
            if response.POST.get("save"):
                for item in ls.item_set.all():
                    if response.POST.get("c" + str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False
                    item.save()
            elif response.POST.get("newItem"):
                txt = response.POST.get('new')
                if len(txt) > 2:
                    ls.item_set.create(text = txt, complete = False)
                else:
                    print("Invalid input")
    
        context = {"ls": ls}
        return render(response, "main/list.html", context)
    else:
        return render(response, "main/view.html", {})


def home(response):
    context = {}
    return render(response, "main/home.html", context)

def create(response):
    if response.user.is_authenticated:
        if response.method == "POST":
            form = CreateNewList(response.POST)
            if form.is_valid():
                n = form.cleaned_data['name']
                t = Todolist(name = n)
                t.save()
                response.user.todolist.add(t)
                #t = Todolist(name = n)
                #t.save()
            return HttpResponseRedirect("/%i" %t.id)
        else:
            form = CreateNewList()
        context = {"form": form}
        return render(response, "main/create.html", context)
    else:
        return render(response, 'registration/login.html', {})

def view(response):
    
    context = {}
    return render(response, "main/view.html", context)

def log_out(response):
    logout(response)
    context = {}
    return render(response, "main/logout.html", context)

def log_in(response):
    if response.method == "POST":
        username = response.POST.get("username")
        password = response.POST.get("password")
        user = authenticate(username = username, password = password)

        if user is not None:
            #correct username and password, login the user
            login(response, user)
            return render(response, "main/home.html", {})