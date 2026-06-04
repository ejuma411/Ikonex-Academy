from django.shortcuts import render, redirect, get_object_or_404
from accounts.decorators import staff_required
from .models import Subject, ClassSubject
from .forms import SubjectForm, ClassSubjectForm


@staff_required
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subjects/list.html', {'subjects': subjects})


@staff_required
def subject_detail(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    assignments = subject.classsubject_set.select_related("class_stream").all()
    return render(request, 'subjects/detail.html', {
        'subject': subject,
        'assignments': assignments,
    })


@staff_required
def subject_create(request):
    form = SubjectForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('subject_list')
    return render(request, 'subjects/create.html', {'form': form})


@staff_required
def subject_update(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    form = SubjectForm(request.POST or None, instance=subject)
    if form.is_valid():
        form.save()
        return redirect('subject_list')
    return render(request, 'subjects/update.html', {'form': form})


@staff_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == "POST":
        subject.delete()
        return redirect('subject_list')
    return render(request, 'subjects/delete.html', {'subject': subject})


# CLASS-SUBJECT ASSIGNMENT
@staff_required
def assign_subject(request):
    form = ClassSubjectForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('subject_list')
    return render(request, 'subjects/assign.html', {'form': form})
