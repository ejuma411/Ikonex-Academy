from django.shortcuts import render, redirect, get_object_or_404
from accounts.decorators import staff_required
from .models import Student
from .forms import StudentForm
from classes.models import ClassStream


@staff_required
def student_list(request):
    students = Student.objects.select_related('class_stream').all()
    return render(request, 'students/list.html', {'students': students})


@staff_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/detail.html', {'student': student})


@staff_required
def student_create(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'students/create.html', {'form': form})


@staff_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'students/update.html', {'form': form})


@staff_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        return redirect('student_list')
    return render(request, 'students/delete.html', {'student': student})
