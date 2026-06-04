from django.shortcuts import render, redirect, get_object_or_404
from .models import ClassStream
from .forms import ClassStreamForm


def class_list(request):
    classes = ClassStream.objects.all()
    return render(request, 'classes/list.html', {'classes': classes})


def class_detail(request, pk):
    class_stream = get_object_or_404(ClassStream, pk=pk)
    students = class_stream.students.all()
    subjects = class_stream.classsubject_set.select_related('subject').all()
    return render(request, 'classes/detail.html', {
        'class_stream': class_stream,
        'students': students,
        'subjects': subjects,
    })


def class_create(request):
    form = ClassStreamForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('class_list')
    return render(request, 'classes/create.html', {'form': form})


def class_update(request, pk):
    class_stream = get_object_or_404(ClassStream, pk=pk)
    form = ClassStreamForm(request.POST or None, instance=class_stream)
    if form.is_valid():
        form.save()
        return redirect('class_list')
    return render(request, 'classes/update.html', {'form': form})


def class_delete(request, pk):
    class_stream = get_object_or_404(ClassStream, pk=pk)
    if request.method == "POST":
        class_stream.delete()
        return redirect('class_list')
    return render(request, 'classes/delete.html', {'class_stream': class_stream})
