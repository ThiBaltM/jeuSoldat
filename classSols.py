class Herbe:
    def __init__(self):
        self.traversableB = True
        self.traversable = True

    def __str__(self):
        return 'h'
    
    
class Wall:
    def __init__(self):
        self.traversableB = False
        self.traversable = False

    def __str__(self):
        return 'w'

class Water:
    def __init__(self):
        self.traversableB = True
        self.traversable = False

    def __str__(self):
        return 'e'

class Tent:
    def __init__(self):
        self.traversableB = False
        self.traversable = False
    
    def __str__(self):
        return 't'
