from django.urls import path
from . import views

urlpatterns = [
    path('', views.sudoku_view, name='sudoku'),
    path('', views.sudoku_solver_view, name='sudoku_solver'),
]
