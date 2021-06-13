from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.views.generic import UpdateView, CreateView, DeleteView
from .models import Question, Choice
from .forms import CreateForm


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


class QuestionUpdateView(UpdateView):
    model = Question
    fields = ['question_text']
    template_name = 'polls/question_update_form.html'


class ChoiceUpdateView(UpdateView):
    model = Choice
    fields = ['question', 'choice_text']
    template_name = 'polls/choice_update_form.html'


class ChoiceCreateView(CreateView):
    model = Choice
    fields = ['question', 'choice_text']
    template_name = 'polls/choice_create_form.html'


class QuestionDeleteView(DeleteView):
    model = Question
    pk_url_kwarg = "question_id"
    success_url = '/polls/'
    template_name = 'polls/question_delete_form.html'


class ChoiceDeleteView(DeleteView):
    model = Choice
    pk_url_kwarg = "choice_id"
    success_url = '/polls/'
    template_name = 'polls/choice_delete_form.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "No choice made",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def create_form(request):
    return render(request, 'polls/create_form.html')


def create(request):
    error = ''
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('polls:success_saved'))
        else:
            error = 'Error'
    form = CreateForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'polls/create.html', data)


def success_saved(request):
    return render(request, 'polls/success_saved.html')

