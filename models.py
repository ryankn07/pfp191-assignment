BOARD_SIZE=10

class Ship:
    def __init__(self,name,length,positions):
        self.name=name
        delf.length=length
        self.positons=positions
        self.hit=[]
    
    def is_sunk(self):
        return len(self.hit)==len(self.positions)


class Board:
    def __init__(self,size=BOARD_SIZE):
        self.size=size
        self.ships=[]     # các tàu bị phá
        self.ship_at={}
        self.shots={}
    
    def is_inside(row,col):
        if 0<row<self.size and 0<col<self.size:
            return True
        else:
            return False
    
    def place_ship(self,name,length,row,col,direction):
        
class Player:
    def __init__(self, player_id, name):
        self.player_id = player_id
        self.name = name