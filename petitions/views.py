from django.shortcuts import render, redirect, get_object_or_404
from .models import Petition, VoteBallot
from .forms import PetitionForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    search_term = request.GET.get('search')
    if search_term:
        petitions = Petition.objects.filter(name__icontains=search_term)
    else:
        petitions = Petition.objects.all()
    template_data = {}
    template_data['title'] = 'Petitions'
    template_data['petitions'] = petitions.order_by("-vote")
    return render(request, 'petitions/index.html', {'template_data': template_data})

def show(request, id):
    petition = Petition.objects.get(id=id)
    template_data = {}
    template_data['title'] = petition.name
    template_data['petition'] = petition
    return render(request, 'petitions/show.html', {'template_data': template_data})

@login_required
def create_petition(request):
    # if request.method == 'POST' and request.POST['title'] != '':
    #     petition = Petition()
    #     petition.name = request.POST['title']
    #     petition.vote = 0
    #     petition.description = request.POST['description']
    #     petition.image = petition
    #     petition.user = request.user
    #     petition.save()
    #     return redirect('petitions.show', id=petition.id)
    # else:
    #     return redirect('petitions.index', id=id)
    if request.method == 'POST':
        petition = Petition()
        petition.user = request.user
        petition.vote = 0
        petition.save()
        form = PetitionForm(request.POST, request.FILES, instance=petition)
        if form.is_valid():
            form.save()
            return redirect('petitions.show', id=petition.id)
    else:
        form = PetitionForm() 
    return render(request, 'petitions/petition_form.html', {'form': form})

@login_required
def edit_petition(request, id):
    petition = get_object_or_404(Petition, id=id)
    # if request.user != petition.user:
    if request.user != petition.user:
        return redirect('petitions.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Petition'
        template_data['petition'] = petition
        form = PetitionForm(instance=petition)
        return render(request, 'petitions/petition_form.html', {'template_data': template_data, 'form': form})
    elif request.method == 'POST':
        form = PetitionForm(request.POST, request.FILES, instance=petition)
        if form.is_valid():
            form.save()
            return redirect('petitions.show', id=petition.id)
    else:
        return redirect('petitions.show', id=id)
    
@login_required
def delete_petition(request, id):
    petition = get_object_or_404(Petition, id=id)
    petition.delete()
    return redirect('petitions.index')

@login_required
def upvote(request, id):
    petition = Petition.objects.get(id=id)
    petitionVotes = VoteBallot.objects.filter(voter=request.user, petition=petition)
    if not petitionVotes:
        petition.vote += 1
        petition.save()

        vote = VoteBallot()
        vote.value = 1
        vote.voter = request.user
        vote.petition = petition
        vote.save()
    else:
        for vote in petitionVotes:
            if vote.value == -1:
                petition.vote += 2
                petition.save()

                vote.value = 1
                vote.save()
    return show(request, id)

@login_required
def downvote(request, id):
    petition = Petition.objects.get(id=id)
    petitionVotes = VoteBallot.objects.filter(voter=request.user, petition=petition)
    if not petitionVotes:
        petition.vote -= 1
        petition.save()

        vote = VoteBallot()
        vote.value = -1
        vote.voter = request.user
        vote.petition = petition
        vote.save()
    else:
        for vote in petitionVotes:
            if vote.value == 1:
                petition.vote -= 2
                petition.save()

                vote.value = -1
                vote.save()
    return show(request, id)