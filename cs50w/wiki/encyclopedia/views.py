import re
import random
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
import markdown2
from .forms import Create, EditPage
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, article):
    if not util.get_entry(article):
        return render(request, "encyclopedia/error.html", {
            "error": "Not found"
        })
    return render(request, "encyclopedia/entry.html", {
        "entry": article,
        "article": markdown2.markdown(util.get_entry(article))
    })

def create(request):
    if request.method == 'POST':
        form = Create(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if util.get_entry(title):
                return render(request, "encyclopedia/error.html", {
                    "error": "An article with that name already exists."
                })
            else:
                util.save_entry(title, content)
                return redirect('entry', title)
    elif request.method == 'GET':
        form = Create(initial={f'content': '# ' + 'Heading 1' + '\n' + 'Body'})

    return render(request, "encyclopedia/create.html", {
        'form': form
    })

def search(request):
    results = []
    query = request.GET.get('q')
    entries = util.list_entries()
    if util.get_entry(query):
        return redirect('entry', query)
    for article in entries:
        match = re.match(query, article, re.IGNORECASE)
        if match:
            results.append(article)
    return render(request, "encyclopedia/results.html", {
                'results': results, 'query': query
                })

def edit(request, title):
    editform = EditPage(initial={'title': title, 'content': util.get_entry(title)})
    if request.method == 'POST':
        editform = EditPage(request.POST)
        if editform.is_valid():
            title = editform.cleaned_data['title']
            content = editform.cleaned_data['content']
            util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", args=(title,)))
    return render(request, 'encyclopedia/edit.html', {'form': editform, 'title': title})

def random_page(request):
    entries = util.list_entries()
    selected_page = random.choice(entries)
    return HttpResponseRedirect(reverse("entry", args=(selected_page,)))
