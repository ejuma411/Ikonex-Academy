from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from accounts.decorators import staff_required
from .models import ClassStream
from .forms import ClassStreamForm


@staff_required
def class_list(request):
    classes = ClassStream.objects.annotate(
        student_count=Count('students')
    ).order_by('name')
    return render(request, 'classes/list.html', {'classes': classes})


@staff_required
def class_detail(request, pk):
    class_stream = get_object_or_404(ClassStream, pk=pk)
    students = class_stream.students.all().order_by('last_name', 'first_name')
    subjects = class_stream.class_subjects.select_related('subject').all()
    return render(request, 'classes/detail.html', {
        'class_stream': class_stream,
        'students': students,
        'subjects': subjects,
    })


@staff_required
def class_create(request):
    form = ClassStreamForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('class_list')
    return render(request, 'classes/create.html', {'form': form})


@staff_required
def class_update(request, pk):
    class_stream = get_object_or_404(ClassStream, pk=pk)
    form = ClassStreamForm(request.POST or None, instance=class_stream)
    if form.is_valid():
        form.save()
        return redirect('class_list')
    return render(request, 'classes/update.html', {'form': form})


@staff_required
def class_delete(request, pk):
    class_stream = get_object_or_404(ClassStream, pk=pk)
    if request.method == "POST":
        class_stream.delete()
        return redirect('class_list')
    return render(request, 'classes/delete.html', {'class_stream': class_stream})
