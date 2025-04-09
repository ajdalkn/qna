from django.urls import path, include
from .views import (
    HomeView, QuestionCreateView, QuestionDetailView, LikeAnswerView
)

urlpatterns = [
    path('api/', include('qna.api.urls')),
    path('', HomeView.as_view(), name='home'),
    path('ask/question/', QuestionCreateView.as_view(), name='ask-question'),
    path('question/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('answer/<int:pk>/like/', LikeAnswerView.as_view(), name='like-answer'),

]