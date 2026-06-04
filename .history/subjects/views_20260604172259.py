from django.shortcuts import render, redirect, get_object_or_404
from .models import Subject, ClassSubject
from .forms import SubjectForm, ClassSubjectForm


def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subjects/list.html', {'subjects': subjects})


def subject_detail(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    return render(request, 'subjects/detail.html', {'subject': subject})


def subject_create(request):
    form = SubjectForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('subject_list')
    return render(request, 'subjects/create.html', {'form': form})


def subject_update(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    form = SubjectForm(request.POST or None, instance=subject)
    if form.is_valid():
        form.save()
        return redirect('subject_list')
    return render(request, 'subjects/update.html', {'form': form})


def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == "POST":
        subject.delete()
        return redirect('subject_list')
    return render(request, 'subjects/delete.html', {'subject': subject})


# CLASS-SUBJECT ASSIGNMENT
def assign_subject(request):
    form = ClassSubjectForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('subject_list')
    return render(request, 'subjects/assign.html', {'form': form})