from django.urls import include, path

urlpatterns = [
    path('v1/', include('qna.api.v1.urls')),

]
