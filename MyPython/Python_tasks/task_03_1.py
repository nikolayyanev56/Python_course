from math import log2
class Player:
    def __init__(self, name , hp , xp, level):
        self._name = name
        self.hp = hp
        self.xp = xp
        self._level = level
    
    def __repr__(self):
        return f"Player(name={self._name}, hp={self.hp}, xp={self.xp}, level={self.level})"
    
    def level_up(self):
        if self.xp <= 300:
            self.level = 1
        elif self.xp > 300: self.level = (2 + log2(int(self.xp / 300)))