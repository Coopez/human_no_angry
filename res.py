# resource fucntions
import numpy as np
import random


def dice():
    return random.randint(1,6)


def house_stuffed(house):
    for n in range(len(house)-1):    
        if house[n] ==1:
           if sum([house[i] for i in range(n,len(house))]) < len(house) - n:
                return False
    return True

def find_pos(player,ground):
    pos = []
    for i in range(len(ground)):
        if ground[i] == player:
            pos.append(i)
    return pos 
    
class Player():
    def __init__(self,number):
        self.number = number
        self.house = [-1,-1,-1,-1]
        self.reserve = 4
        self.placement = 0
    
    def win(self):
        return sum(self.house) == 4
    
    def turn(self,ground,killed):
        
        #print("DEBUG")
        #print( self.reserve)
        self.reserve += sum([1 for i in killed if i==self.number]) # add own killed to reserve
        #print( "ADDED TO RESERVE: "+str(sum([1 for i in killed if i==self.number])))
        killed = [kill for kill in killed if kill!=self.number] # delete these from killed list
        
        if (house_stuffed(self.house) and sum(self.house)+self.reserve == 4 ) or self.reserve == 4:
            throws = 3
        else: 
            throws = 1
        while throws != 0:
            throw = dice()
            own_pos = find_pos(self.number,ground)
            ground, kill = self.descision(ground,own_pos,throw)
            if throw == 6:  
                throws = 1
            else: 
                throws -= 1
            if kill > -1:    
                killed.append(kill)

        return ground,killed
    
    def debug(self,ground):
        counter= sum([1 for item in ground if item == self.number])
        print("Player: " + str(self.number))
        print("On the field are: " + str(counter))
        print("Reserve: " + str(self.reserve))
        print(ground)
        h = sum([1 for item in self.house if item==1])
        assert counter+self.reserve+h == 4
        return
    


    def descision(self,ground,position,throw):
        if ground[self.number*10] == self.number and self.reserve>0 and ground[throw+self.number*10]!=self.number: # if there is an own piece at start and reserve is not empty
            kill = ground[throw+self.number*10]
            ground[throw+self.number*10]=self.number 
            ground[self.number*10] = -1
              
            return ground,kill
        if throw == 6 and self.reserve > 0 and ground[self.number*10] != self.number: 
                     # if a six is thrown and a piece can be brought in

            self.reserve -= 1
            kill = ground[self.number*10]
            ground[self.number*10] = self.number
            return ground,kill

        moves = [i+ throw for i in position] # determine preference and legality of remaining moves
        finish_line = self.number*10 - 1
        if finish_line == -1:
            finish_line = len(ground)-1
        legal_moves =[]
        for move in moves:
            
            if (move - throw < finish_line and  move > finish_line) or (move >= len(ground)-1 and self.number==0):
                house_reach = move - finish_line
                if house_reach <= 4 and self.house[house_reach-1] ==-1:
                    
                    ground[move-throw] = -1
                    self.house[house_reach-1] = 1
                    return ground, -1
                else:
                    continue
                
            if move >= len(ground):
                move -= len(ground)
                
            if ground[move] != self.number:
                #print("DEBUG") 
                if ground[move] != -1:
                    kill = ground[move]
                    ground[move] = self.number
                    assert ground[move-throw] == self.number
                    ground[move-throw] = -1
                    return ground, kill
                elif ground[move] == -1:
                    legal_moves.append(move)
        
        if legal_moves:
            #print("DEBUG")
            legal_moves_diff = [finish_line-i for i in legal_moves]
            move = legal_moves[legal_moves_diff.index(max(legal_moves_diff))]
            ground[move] = self.number
            #print(move)
            #print(throw)
            assert ground[move-throw] == self.number
            ground[move-throw] = -1
            #self.debug(ground)
        return ground, -1        

        # list goes from 0 to 38
