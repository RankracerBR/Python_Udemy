from PySide6.QtWidgets import QPushButton, QGridLayout, QWidget
from PySide6.QtCore import Slot
from variables import MEDIUM_FONT_SIZE
from utils import isNumOrDot, isEmpty, isValidNumber
from display import Display
import math


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()
    
    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)
        self.setCheckable(True)

class ButtonsGrid(QGridLayout):
    def __init__(self, display: Display, info, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ['C', 'D', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['N',  '0', '.', '='],
        ]
        self.display = display
        self.info = info
        self._equation = ''
        self._equationInitialValue = 'Sua conta'
        self._left = None
        self._right = None
        self._op = None
        self._makeGrid()
    
    @property
    def equation(self):
        return self._equation
    
    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):
        for row_number , row_data in enumerate(self._gridMask):
            for column_number, button_text in enumerate(row_data):
                #print('Linha', row_number, 'Coluna', column_number, button_text)
                button = Button(button_text)

                if not isNumOrDot(button_text) and not isEmpty(button_text):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)

                self.addWidget(button, row_number, column_number)
                slot = self._makeSlot(self._insertButtonTextToDisplay,button)
                self._connectButtonClicked(button, slot)

    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        text = button.text()
        
        if text == 'C':
            self._connectButtonClicked(button, self._clear)
            # button.clicked.connect(self.display.clear)
        
        if text in '+-/*^':
            self._connectButtonClicked(
                button, 
                self._makeSlot(self._operatorClicked, button)
            )
        
        if text in '=':
            self._connectButtonClicked(button, self._eq)

    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot

    def _insertButtonTextToDisplay(self,button):
        buttonText = button.text()
        newDisplayValue = self.display.text() + buttonText
        if not isValidNumber(newDisplayValue):
            return 

        self.display.insert(buttonText)

    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitialValue
        self.display.clear()
    
    def _operatorClicked(self, button):
        buttonText = button.text() # +-/* (etc)
        displayText = self.display.text() # Deverá ser meu número _left
        self.display.clear()

        # Se a pessoa clicou no operador sem
        # confuigurar qualquer número
        if not isValidNumber(displayText) and self._left is None:
            print('Não tem nada para colocar no valor da esquerda')
            return

        # Se houver algo no número da esquerda,
        # não fazemos nada. Aguardaremos o número da direita.

        if self._left is None:
            self._left = float(displayText)
        
        self._op = buttonText
        self.equation = f'{self._left} {self._op} ??'
    
    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            print('Sem nada para a direita')
            return

        self._right = float(displayText)
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 'error'
        
        try:
            if '^' in self.equation and isinstance(self._left, float): # Afunilamento de Tipagem
                result = math.pow(self._left, self._right)
            else:
                result = eval(self.equation) # eval() avalia uma string como código python, CUIDADO!
        except ZeroDivisionError:
           print('Zero Division Error')
        except OverflowError:
            print('Número muito grande')

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left = result
        self._right = None

        if result == 'error':
            self._left = None