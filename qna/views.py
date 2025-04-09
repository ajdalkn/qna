from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView
from django.views import View
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, redirect

from .forms import QuestionForm, AnswerForm
from .models import Question, Answer, Like


class HomeView(TemplateView):
    template_name = 'qna/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.all().order_by(
            '-created_on')
        return context


class QuestionCreateView(LoginRequiredMixin, FormView):
    template_name = 'qna/ask_question.html'
    model = Question
    form_class = QuestionForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        question = form.save(commit=False)
        question.user = self.request.user
        question.created_by = self.request.user
        question.modified_by = self.request.user
        question.save()
        return super().form_valid(form)


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'qna/question_detail.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context.update({
            'answers': self.object.answers.all().order_by('-created_on'),
            'form': AnswerForm(),
            'user_answered': self.object.answers.filter(
            user=self.request.user).exists() if user.is_authenticated else False,
        })

        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        self.object = self.get_object()
        form = AnswerForm(
            user=request.user, question=self.get_object(), data=request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = self.object
            answer.user = request.user
            answer.created_by = request.user
            answer.modified_by = request.user
            answer.save()
            return redirect(
                reverse('question-detail', kwargs={'pk': self.object.pk}))

        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class LikeAnswerView(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        answer = get_object_or_404(Answer, pk=pk)
        return redirect('question-detail', pk=answer.question.pk)

    def post(self, request, pk, *args, **kwargs):
        answer = get_object_or_404(Answer, pk=pk)
        like, created = Like.objects.get_or_create(
            user=request.user, answer=answer)

        if not created:
            # Already liked, so unlike
            like.delete()
        else:
            like.created_by = request.user
            like.modified_by = request.user
            like.save()

        return redirect('question-detail', pk=answer.question.pk)
