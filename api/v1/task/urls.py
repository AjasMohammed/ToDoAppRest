from django.urls import path
from .views import *


urlpatterns = [
    path('addtask/', AddTask.as_view()),
    path('deletetask/<int:pk>', TaskIsDeleted.as_view()),
    path('mark-as-done/<int:pk>', TaskIsDone.as_view()),
    path('view-task/', ViewTask.as_view()),
]