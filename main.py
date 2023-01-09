from res import Player
import numpy as np

## Parameter
playercount = 4


#init players
players=[Player(i) for i in range(0,playercount)]
ground = [-1 for i in range(0,10*playercount-1)]

status = 0 # is getting higher as people finish

killed = []
turncounter = [0 for i in range(playercount)]
while status < playercount:
    
    for player in players:
        if player.placement==0:
            ground,killed = player.turn(ground,killed)
            turncounter[player.number]+=1
            #print("Turn of Player " + str(player.number))
            #print("Current Field: " + str(ground) )
            #print("Current House: "+ str(player.house))
            #print("Current Player Reserve: " + str(player.reserve))
            #print("Current killed: " + str(killed))
            if player.win():
                status+=1
                player.placement=status
                print("Player " + str(player.number) + " finished. ")
print(turncounter)
    #status+=1/2           