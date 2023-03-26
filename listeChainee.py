class Cell:
    def __init__(self, v , n = None):
        self.valeur = v
        self.suivante = n

class Liste:
    def __init__(self):
        self.contenu = None

    def __str__(self):
        res = ''
        c = self.contenu
        compteur = 0
        while c is not None:
            if compteur == 0:
                res = res + f'[{c.valeur},'
            elif compteur == len(self) - 1:
                res = res + f'{c.valeur}]'
            else:
                res = res + f'{c.valeur},'
            c = c.suivante
            compteur += 1
        return res

    def supprVal(self, val):
        """supprime la première valeur val trouvée, ne change rien si il ny a pas de val
        param: : val - valeurs a supprimé"""
        avantC = self.contenu
        c = self.contenu
        while c != None and c.valeur != val:
            avantC = c
            c = c.suivante
        if c != None and c == avantC:
            self.contenu = c.suivante
        elif c != None:
            avantC.suivante = c.suivante

    def append(self, v):
        self.contenu = Cell(v, self.contenu)

    def __getitem__(self, n):
        l = self.contenu
        c = 0
        while c != n and l!=None:
            l = l.suivante
            c += 1
        if l == None:
                raise IndexError("Index out of range")
        return l.valeur

    def __len__(self):
        c = 0
        liste = self.contenu
        while liste != None:
            c+= 1
            liste= liste.suivante
        return c

    def tableau(self):
        """cette fonction renvoie la liste chainée mais sous forme de tableau"""
        t= []
        l = self.contenu
        while l != None:
            t.append(l.valeur)
            l = l.suivante
        return t

    def passable(self):
        """Cette fonction renvoie un booléen True si tout les élmts de la liste on l'attribut traversable a True"""
        for k in self:
            if not k.traversable:
                return False
        return True
    
    def passableB(self):
        """Cette fonction renvoie un booléen True si tout les elmts de la liste on l'attributs traversableB a True"""
        for k in self:
            if not k.traversableB:
                return False
        return True
