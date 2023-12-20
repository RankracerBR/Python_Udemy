class Caneta:
    def __init__(self, cor):
        self.cor = cor #o '_' ou '__' significa para não ser usado(convensão)
        self.cor_tampa = None
    
    @property
    def cor(self):
        print('ESTOU NO GETTER')
        return self._cor

    @cor.setter
    def cor(self, valor):
        print('ESTOU NO SETTER')
        self._cor = valor
      
    @property  
    def cor_tampa(self):
        return self._cor_tampa
    
    @cor_tampa.setter
    def cor_tampa(self, valor):
        self._cor_tampa = valor
    
#def mostrar(caneta):
    #return caneta.cor

caneta = Caneta('Azul')
caneta.cor = 'Rosa'
caneta.cor_tampa = 'Azul'
print(caneta.cor)
print(caneta.cor_tampa)