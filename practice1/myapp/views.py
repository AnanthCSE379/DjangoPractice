from django.shortcuts import render
from .forms import PlayerForm
from .models import Player,Goalkeeper,FieldPlayer


# User-defined exceptions required by the question.
class InvalidPlayerID(Exception):
    pass


class PlayerIDNotMatched(Exception):
    pass


def start(request):
    return render(request,'start.html')


def register(request):
    form = PlayerForm()
    if (request.method == 'POST'):
        form = PlayerForm(request.POST)
        try:
            idx = request.POST.get('id','')
            # A five-digit number must be between 10000 and 99999.
            if (len(idx) != 5 or not idx.isdigit() or not idx.isascii() or idx[0] == '0'):
                raise InvalidPlayerID('Invalid PlayerID')
            if (Player.objects.filter(id=int(idx)).exists()):
                raise InvalidPlayerID('Invalid PlayerID')

            if (form.is_valid()):
                player = form.save(commit=False)
                score = form.cleaned_data['score']
                if (player.player_type == 'Goalie'):
                    details = Goalkeeper(player.name,player.id,player.count,score)
                    player.TotalStoppingShots = details.TotalStoppingShots
                else:
                    details = FieldPlayer(player.name,player.id,player.count,score)
                    player.GoalCount = details.GoalCount
                player.save()
                return render(request,'message.html',context={
                    'message':'Successfully inserted', 'next_page':'start'
                })
        except InvalidPlayerID as error:
            return render(request,'message.html',context={
                'message':str(error), 'next_page':'register'
            })
    return render(request,'register.html',context={'form':form})


def display(request):
    players = Player.objects.all()
    return render(request,'players.html',context={'players':players})


def searchplayer(request):
    if (request.method == 'POST'):
        try:
            idx = request.POST.get('id','')
            if (len(idx) != 5 or not idx.isdigit() or not idx.isascii()):
                raise PlayerIDNotMatched('PlayerID Not Matched')
            player = Player.objects.filter(id=int(idx)).first()
            if (player is None):
                raise PlayerIDNotMatched('PlayerID Not Matched')
            return render(request,'players.html',context={
                'players':[player], 'title':'Search Result'
            })
        except PlayerIDNotMatched as error:
            return render(request,'message.html',context={
                'message':str(error), 'next_page':'searchplayer'
            })
    return render(request,'search.html')


def findbest(request):
    best = None
    searched = False
    if (request.method == 'POST'):
        searched = True
        player_type = request.POST.get('player_type','')
        players = Player.objects.filter(player_type=player_type).order_by('id')
        # Goalie: compare stop rates. Field Player: compare goal counts.
        for player in players:
            if (best is None):
                best = player
            elif (player_type == 'Goalie' and player.stoprate() > best.stoprate()):
                best = player
            elif (player_type == 'Field Player' and player.GoalCount > best.GoalCount):
                best = player
    return render(request,'bestplayer.html',context={'best':best, 'searched':searched})
