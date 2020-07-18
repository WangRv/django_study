from django.shortcuts import (render,
                              get_object_or_404)
from django.http import (HttpResponse,
                         HttpResponseRedirect,
                         Http404)
from django.urls import reverse
from django.views import generic
# model importation
from .models import (Question,
                     Choice)


class IndexView(generic.ListView):
    template_name = "home/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "home/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "home/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "home/detail.html", {
            "question": question,
            "error_message": "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1  # vote this item
        selected_choice.save()
        return HttpResponseRedirect(reverse("home:results", args=(question_id,) ))
