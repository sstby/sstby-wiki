from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
import markdown2
import random
from . import util

class NewPageForm(forms.Form):
    form_title = forms.CharField(label="Article name:")
    form_body = forms.CharField(label="Article body in markdown format", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def page(request, title):    
    if title.lower() in util.to_lower_case(util.list_entries()):
        return render(request, "encyclopedia/pages.html", {
            "title": title,
            "pbody": markdown2.markdown(util.get_entry(title))
        })
    else:
        return render(request, "encyclopedia/errorpage.html", {
        "message": str("Sorry, this page is not created yet.")
    })

def search(request):
    query = request.GET.get('q', '')
    if util.get_entry(query) is not None:
        return HttpResponseRedirect(reverse("wiki:page", args=(query,)))
    else:
        coincidence_list = []
        names = util.to_lower_case(util.list_entries())
        for text in names:
            if query != '' and query.lower() in text:
                coincidence_list.append(text.capitalize())
        if not coincidence_list:
            return render(request, "encyclopedia/errorpage.html", {
        "message": str("No results were found for your query.")
    })
        else:
            return render(request, "encyclopedia/search.html", {
                "title": str("Search results"),
                "results": coincidence_list,
                "query": query
            })

def newpage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        title = request.POST.get('form_title')
        body = request.POST.get('form_body')
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/errorpage.html", {
        "message": str("This page is allready created.")
    })
        else:
            if form.is_valid(): 
                util.save_entry(title, body)
                return HttpResponseRedirect(reverse("wiki:page", args=(title,)))
    return render(request, "encyclopedia/newpage.html", {
        "form": NewPageForm
    })

def edit(request, title):
    body = util.get_entry(title)
    names = util.list_entries()
    names.remove(title)
    if request.method == "POST":
        form = NewPageForm(request.POST)
        new_title = request.POST.get('form_title')
        new_body = request.POST.get('form_body') 
        if new_title in names:
            print(names)
            return render(request, "encyclopedia/edit.html", {
                "error": str("Trying to change another article!"),
                "form": form,
                "title": title
                })
        if form.is_valid():
            util.save_entry(new_title, new_body)
            return HttpResponseRedirect(reverse("wiki:page", args=(new_title,)))
    form = NewPageForm(initial={'form_title': title, 'form_body': body})
    return render(request, "encyclopedia/edit.html", {
        "form": form,
        "title": title
    })

def randompage(request):
    title = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("wiki:page", args=(title,)))