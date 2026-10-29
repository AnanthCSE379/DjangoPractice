from django.db import models


# Ordinary Python classes for inheritance. They do not create database tables.
class Human:
    def __init__(self,name,idx,count):
        self.name = name
        self.id = idx
        self.count = count


class Goalkeeper(Human):
    def __init__(self,name,idx,count,TotalStoppingShots):
        Human.__init__(self,name,idx,count)
        self.TotalStoppingShots = TotalStoppingShots
        if (count == 0):
            self.stoprate = 0
        else:
            self.stoprate = TotalStoppingShots / count


class FieldPlayer(Human):
    def __init__(self,name,idx,count,GoalCount):
        Human.__init__(self,name,idx,count)
        self.GoalCount = GoalCount


# ONE database table for both player types.
class Player(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    player_type = models.CharField(max_length=15,choices=[
        ('Goalie','Goalie'), ('Field Player','Field Player')
    ])
    count = models.PositiveIntegerField()
    TotalStoppingShots = models.PositiveIntegerField(default=0)
    GoalCount = models.PositiveIntegerField(default=0)

    def stoprate(self):
        goalkeeper = Goalkeeper(self.name,self.id,self.count,self.TotalStoppingShots)
        return goalkeeper.stoprate
