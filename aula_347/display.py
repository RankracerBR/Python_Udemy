from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QLineEdit
from utils import isEmpty, isNumOrDot
from variables import BIG_FONT_SIZE, MINIMUN_WIDTH, TEXT_MARGIN
from PySide6.QtCore import Qt, Signal


class Display(QLineEdit):
    eqPressed = Signal()
    delPressed = Signal()
    clearPressed = Signal()
    inputPressed = Signal(str)
    operatorPressed = Signal(str)

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configstyle()

    def configstyle(self):
        margin = [TEXT_MARGIN for _ in range(4)]
        self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px;')
        self.setMinimumHeight(BIG_FONT_SIZE * 2)
        self.setMinimumWidth(MINIMUN_WIDTH)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*margin)
    
    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text().strip() # .strip() remove os espaços da direita e da esquerda
        key = event.key()
        KEYS = Qt.Key

        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return, KEYS.Key_Equal]
        isDelete = key in [KEYS.Key_Backspace, KEYS.Key_Delete, KEYS.Key_D]
        isEsc = key in [KEYS.Key_Escape, KEYS.Key_C]
        isOperator = key in [
            KEYS.Key_Plus, KEYS.Key_Minus, KEYS.Key_Slash, KEYS.Key_Asterisk,
            KEYS.Key_P
            ]

        if isEnter:
            self.eqPressed.emit()
            return event.ignore()      

        if isDelete:
            self.delPressed.emit()
            return event.ignore()       

        if isEsc:
            self.clearPressed.emit()
            return event.ignore()        

        if isOperator:
            if text.lower() == 'p':
                text = '^'
            self.operatorPressed.emit(text)
            return event.ignore()    

        # Não passar daqui
        if isEmpty(text):
            return event.ignore()
    
        if isNumOrDot(text):
            self.inputPressed.emit(text)
            return event.ignore()           
