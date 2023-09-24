from django.shortcuts import render, redirect
from .utils import get_mongo
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import AuthorForm, QuoteForm
from .models import Author, Quote, Tag

# Create your views here.


def main(request, page=1):
    db = get_mongo()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quote_on_page = paginator.page(page)
    return render(request, "quotes/index.html", context={"quotes": quote_on_page})


def author(request, author_name):
    db = get_mongo()
    author = db.author.find_one({"fullname": author_name})
    return render(request, "quotes/author.html", context={"author": author})


@login_required
def author_create(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            new_author = form.save()
            new_author.save()

            return redirect(to="quotes:main")
        else:
            return render(
                request,
                "quotes/author_create.html",
                {"form": form},
            )

    return render(
        request,
        "quotes/author_create.html",
        {"form": AuthorForm()},
    )


@login_required
def quote(request):
    tags = Tag.objects.all()
    all_authors = Author.objects.all()
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist("tags"))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)
            new_quote.author = Author.objects.get(id=request.POST.get("author"))
            new_quote.save()

            return redirect(to="quotes:main")
        else:
            return render(
                request,
                "quotes/quote.html",
                {"tags": tags, "all_authors": all_authors, "form": form},
            )

    return render(
        request,
        "quotes/quote.html",
        {"tags": tags, "all_authors": all_authors, "form": QuoteForm()},
    )
