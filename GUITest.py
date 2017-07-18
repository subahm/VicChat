#Simple proof of concept GUI

import sys
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *

#create our window
app = QApplication(sys.argv)
w = QWidget()
w.setWindowTitle('VicChat GUI prototype')
w.resize(320,310)

#Create a button in the window
btn = QPushButton('Print text to console', w)
btn.move(100,250)

#Create a button to close the program
exitBtn = QPushButton("Click to exit", w)

#Create a useless button
uselessBtn = QPushButton("Useless popup button", w)
uselessBtn.setToolTip("This button is totally useless!")

# Create textbox for data-entry
inputBox = QLineEdit(w)
inputBox.resize(280,20)
inputBox.setPlaceholderText("enter message here")

# Create a multi-line textbox to display history
outputBox = QPlainTextEdit(w)
outputBox.resize(280,170)
outputBox.setReadOnly(True)
outputBox.appendPlainText("""(12:52) Matt: Did anyone get that new chat room button?
(12:55) Bryan: I think the tabs function broke it
(12:58) Matt: Didn't Bob fix that?
(12:59) Bryan: Yeah, but it broke formatting on everything, so we didn't push it
(1:01) Matt: Gotcha
(1:02) Matt: Eta on that Bob?
(1:15) Bob: Working on it, give me a couple hours
(1:18) Matt: Roger""")

#Place everything on the screen
exitBtn.move(115,275)
uselessBtn.move(200,10)
inputBox.move(20, 220)
outputBox.move(20,40)

#           Create the actions:
#
#Prints the message to the message history, and clears the input box
@pyqtSlot()
def on_press_print():
    message = inputBox.text()
    outputBox.appendPlainText("(time) You: " + message)
    inputBox.clear()

#Creates a message box ("warning" type)
@pyqtSlot()
def on_press_useless():
    QMessageBox.warning(w, 'Mwahaha!', "See? Completely useless!")

#Creates a popup to confirm if the user wants to exit the program
@pyqtSlot()
def on_press_exit():
    ans = QMessageBox.question(w, 'Message', "Are you sure you want to quit?",
                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if ans == QMessageBox.Yes:
        exit(0)
    else:
        pass


# connect the signals to the slots
btn.pressed.connect(on_press_print)
exitBtn.pressed.connect(on_press_exit)
uselessBtn.pressed.connect(on_press_useless)

# This locks all keyboard input in the app to this box
# Not a good solution
# inputBox.grabKeyboard()

# Show the window and run the app
w.show()
app.exec_()