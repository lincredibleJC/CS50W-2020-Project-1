import random

import markdown2
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util


class NewEntryForm(forms.Form):
	title = forms.CharField(label="Page Title")
	content = forms.CharField(label="Page Content", widget=forms.Textarea())


def index(request):
	return render(request, "encyclopedia/index.html", {
		"entries": util.list_entries()
	})

def wiki(request, title):
	markdown_text = util.get_entry(title)
	if markdown_text is None:
		return render(request, "encyclopedia/page_not_found.html", {"title": title})
	html_text = markdown2.markdown(markdown_text)
	return render(request, "encyclopedia/wiki.html", {"title": title, "html_text": html_text})

def random_entry(request):
	random_entry = random.choice(util.list_entries())
	return HttpResponseRedirect(reverse("wiki", args=[random_entry]))

def search_entry(request):
	search_results = []
	query = request.POST.get("q")
	entries = util.list_entries()
	for entry in entries:
		if entry.upper() == query.upper():
			return HttpResponseRedirect(reverse("wiki", args=[query]))
		elif query.upper() in entry.upper():
			search_results.append(entry)
	return render(request, "encyclopedia/search_results.html", {"title": query, "search_results": search_results})

def create_entry(request):
	if request.method == "POST":
		form = NewEntryForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data["title"]
			content = form.cleaned_data["content"]

			entry_already_exists = util.get_entry(title) is not None

			if entry_already_exists:
				return render(request, "encyclopedia/create_entry.html", {"title": title, "error": True, "form": form})

			content_with_title = f"# {title}\n\n{content}"
			util.save_entry(title, content_with_title)

			return HttpResponseRedirect(reverse("wiki", args=[title]))
		else:
			return render(request, "encyclopedia/create_entry.html", {"form": form})


	return render(request, "encyclopedia/create_entry.html", {"form": NewEntryForm()})

def edit_entry(request, title):
	if request.method == "POST":
		form = NewEntryForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data["title"]
			content = form.cleaned_data["content"]

			content_with_title = f"# {title}\n\n{content}"
			util.save_entry(title, content_with_title)

			return HttpResponseRedirect(reverse("wiki", args=[title]))
		else:
			return render(request, "encyclopedia/edit_entry.html", {"form": form})

	markdown_text = util.get_entry(title)
	if markdown_text is None:
		return render(request, "encyclopedia/page_not_found.html", {"title": title})

	content = markdown_text.split("\n", 2)[2]
	return render(request, "encyclopedia/edit_entry.html", {"title": title, "form": NewEntryForm(initial={"title": title, "content": content})})
