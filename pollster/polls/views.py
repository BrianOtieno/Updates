from django.http import request
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Question, Choice
from django.urls import reverse

# Create your views here.

def index(request):
    question_list = Question.objects.order_by('-pub_date')[:5]
    context = {"question_list": question_list}
    return render(request, 'polls/index.html', context)

def register(*args, **kwargs):
    return HttpResponse("<h1>Register</h1>")

def details(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    
    return render(request, 'polls/details.html', {'question':question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/details.html', {
            'question' : question,
            'error_message': "No choice selected!"
        })
    else:
        selected_choice.votes +=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
