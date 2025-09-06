import PyQt5.QtWidgets as qtw 
import PyQt5.QtGui as qtg
import random

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        #Add a title 
        self.setWindowTitle("Number Guessing Game ")

        #Set layout 
        layout = qtw.QVBoxLayout() 
        self.setLayout(layout)        

        # Create Label 
        my_label = qtw.QLabel("Guess No btw 0 to 100 ", self)
        my_label.setFont(qtg.QFont('Helvetica',24))
        layout.addWidget(my_label)

        #Entry Box 
        my_entry = qtw.QLineEdit()
        my_entry.setObjectName("Number_field")
        my_entry.setPlaceholderText("Enter the no.")
        my_entry.setValidator(qtg.QIntValidator(0,100,self))
        layout.addWidget(my_entry)

        no = random.randint(0,100) 


        #create a button 
        my_button = qtw.QPushButton("Check")
        my_button.clicked.connect(lambda: press_it())
        my_button.setObjectName("my_button")
        layout.addWidget(my_button)

        def press_it():
            text = my_entry.text()
            if not text:
                my_label.setText("Enter a number")
                return
            integar_value = int(text)
            if integar_value > no:
                my_label.setText("Too High")
            elif integar_value < no:
                my_label.setText("Too Low")
            else:
                my_label.setText("You Got it")

        self.show()

app = qtw.QApplication([])
mw  = MainWindow()

app.exec_()
