class Polynome:
    """Pour créer un polynome on part du terme constant pour aller vers le
    terme préponderant en incrémentant la puissance de X de 1 pour chaque indice 
    de la liste."""
    def __init__(self, L):
        self.liste_coef = L
        if L == [0]: self.degre = False
        else : self.degre = len(L)

    def evaluation(self, z):
        resultat = 0
        for i in range(self.degre):
            resultat = resultat + self.liste_coef[i]*z**i
        return resultat
    
    def derive(self):
        nouvelle_liste = [[0] for i in range(len(self.liste_coef))]
        for i in range(len(nouvelle_liste)):
            nouvelle_liste[i] = self.liste_coef[i]*i
        for i in range(1, len(nouvelle_liste)):
            nouvelle_liste[i-1] = nouvelle_liste[i]
        nouvelle_liste.pop()
        return Polynome(nouvelle_liste)

    def show(self):
        chaine = f"P(X) = "
        for i in range(len(self.liste_coef)):
            chaine += f"{self.liste_coef[i]}*X^{i} + "
        print(chaine)

    def additionner(PA, PZ):
        taille = max(len(PA.liste_coef), len(PZ.liste_coef))
        nouvelle_liste = [[0] for i in range(taille)]
        for i in range(taille):
            try:
                x = PA.liste_coef[i]
            except:
                x = 0
            try:
                y = PZ.liste_coef[i]
            except:
                y = 0
            nouvelle_liste[i] = x + y
        print(nouvelle_liste)
        return Polynome(nouvelle_liste)

P1 = Polynome([2, 3, 8])
P1.show()
P2 = P1.derive()
P2.show()

Polynome.additionner(P1, P2).show()


    

