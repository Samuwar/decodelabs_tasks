####### QUIZ APP ##########
import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QLineEdit, QGridLayout, QRadioButton, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt, QEvent

class mainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Quiz App")
        self.setGeometry(100, 50, 500, 500)
        
        self.init_UI()      # recallable initial UI
        
    def init_UI(self):
        """Load when the class initiates and also re-initialize class"""
        self.grid = QGridLayout(self)
        
        self.name_label = QLabel("Name: ", self)
        self.name_label.setFixedWidth(100)
        self.input_box = QLineEdit(self)
        self.input_box.setFixedWidth(200)
        self.submit_btn = QPushButton("Take Quiz", self)
        self.submit_btn.setFixedWidth(100)
        self.add_question_btn = QPushButton("Set Quiz", self)
        self.add_question_btn.setFixedWidth(100)
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        self.num = 0
        self.user_name = ""
        self.answers = []
        self.score_counter = 0
        self.file_path = 'quiz.json'
        
        try:
            with open(self.file_path, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {"questions": []}
            with open(self.file_path, 'w') as file:
                json.dump(self.data, file)
                
        self.questions = self.data["questions"]
        
        # self.input_box.setPlaceholderText("Enter your name")
        
        self.submit_btn.clicked.connect(self.init_quiz_input)
        self.add_question_btn.clicked.connect(self.init_set_question)
        
        ##### SET BASE ROWS AND COLUMNS #########
        self.empty_label = QLabel("", self)
        self.grid.addWidget(self.empty_label, 10, 6)
        
        self.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    font-style: Arial;
                    margin-top: 30px;
                    padding: 5px;
                    border: 1px solid black;
                    border-radius: 15px;
                    background-color: rgb(220, 220, 220);
                }
                QPushButton::hover {
                    background-color: transparent
                }
                QLineEdit {
                    font-size: 16px;
                    margin-left: 0;
                    padding-left: 5px;
                    border: none;
                    border-bottom: 1px solid;
                    background-color: transparent;
                }
                           """)
        self.grid.addWidget(self.name_label, 4, 0, 5, 3, Qt.AlignmentFlag.AlignRight)
        self.grid.addWidget(self.input_box, 4, 3, 5, 4, Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(self.submit_btn, 4, 2, 6, 1)
        self.grid.addWidget(self.add_question_btn, 4, 4, 6, 1)
        
        self.widget = QWidget()
        self.widget.setLayout(self.grid)
        self.setCentralWidget(self.widget)
    
    def init_quiz_input(self):
        self.user_name = self.input_box.text()
        self.get_quiz()
        
    def init_set_question(self):
        self.user_name = self.input_box.text()
        self.set_question()
    
    def get_quiz(self):
        """Get the quiz questions and display them"""
        self.clear_layout(self.grid)
        self.grid = QGridLayout(self)
        self.hlayout = QHBoxLayout()
        self.name_label = QLabel(self.user_name, self)
        self.name_label.setObjectName("name_label")
        self.grid.addWidget(self.name_label, 1, 4, 1, 3, Qt.AlignmentFlag.AlignCenter)
        self.question_label = QLabel("",self)
        self.question_label.setWordWrap(True)
        self.question_label.setFixedSize(500, 100)
        
        question = {}
        try: question = self.questions[self.num]
        except IndexError: self.error = QLabel("No Question Found")
        self.input_answer = QLineEdit(self)
        self.input_answer.setVisible(False)
         
        if question: 
            self.question_label.setText(f"<b>Question:</b> {question['question']}")
            self.grid.addWidget(self.question_label, 3, 5, Qt.AlignmentFlag.AlignLeft)
            self.question_label.setObjectName("question_label")
            if len(question['options']) > 0:
                self.option_label = QLabel(f"<b>Options: </b>")
                self.grid.addWidget(self.option_label, 4, 5)
                for index, option in enumerate(question['options']):
                    self.letters[index] = QRadioButton(str(option), self)
                    for answer in self.answers:
                        if self.num == answer['quest_num'] and str(answer['answer']).strip().lower() == str(option).strip().lower(): self.letters[index].setChecked(True)
                    self.letters[index].toggled.connect(self.send_option)
                    self.grid.addWidget(self.letters[index], index + 5, 5, Qt.AlignmentFlag.AlignLeft)
            else:
                self.input_answer.setVisible(True)
                self.input_answer.installEventFilter(self)
                self.input_answer.setFixedSize(400, 50)
                self.input_answer.setPlaceholderText("Enter Your Answer")
                for answer in self.answers:
                    if self.num == answer['quest_num']: self.input_answer.setText(answer['answer'])
                self.grid.addWidget(self.input_answer, 5, 5, Qt.AlignmentFlag.AlignLeft)
        else:
            self.error.setFixedSize(500, 80)
            self.grid.addWidget(self.error, 3, 5)     
            
        self.prev_btn = QPushButton("Prev", self)
        self.prev_btn.setFixedSize(70, 70)
        self.next_btn = QPushButton("Next", self)
        self.next_btn.setFixedSize(70, 70)
        self.submit_btn = QPushButton("Submit", self)
        self.submit_btn.setFixedSize(100, 70)
        self.grid.addWidget(self.submit_btn, 11, 5, Qt.AlignmentFlag.AlignCenter)
        self.submit_btn.setEnabled(True) if len(self.answers) == len(self.questions) else self.submit_btn.setEnabled(False)
        self.submit_btn.clicked.connect(self.submit_quiz)
        
        if self.num == 0: self.prev_btn.setDisabled(True)
        if self.num == len(self.questions) - 1: self.next_btn.setDisabled(True)
        self.prev_btn.clicked.connect(self.prev_question)
        self.next_btn.clicked.connect(self.next_question)
        
        self.grid.addWidget(self.prev_btn, 10, 5, Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(self.next_btn, 10, 5, Qt.AlignmentFlag.AlignRight)       
        
        self.setStyleSheet("""                
                QPushButton{
                    font-size: 16px;
                    width: 80px;
                    border: .5px solid rgb(200, 200, 200);
                    border-radius: 5px;
                    margin-top: 32px;
                    padding: 5px;
                }
                QLabel {
                    font-size: 16px;
                    font: Arial;
                    height: 20px;
                }
                QLabel#name_label{
                    font-size: 32px;
                    padding: 5px;
                    margin-bottom: 10px;
                }
                
                QLabel#question_label {
                    margin-bottom: 32px;
                }
                
                QRadioButton {
                    font-size: 16px;
                    padding: 5px;
                    margin-top: 0;
                }
                QLineEdit {
                    font-size: 16px;
                    padding: 5px;
                    background-color: transparent;
                    border: none;
                    border-bottom: 1px solid black;
                }
                           
                           """)
        
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.widget = QWidget()
        self.widget.setLayout(self.grid)
        self.setCentralWidget(self.widget)

    def send_option(self):
        response = self.sender()
        if response.isChecked(): self.record_answer(response.text())
        
        #Enable submit button after attempting all questions
        if not self.submit_btn.isEnabled() and len(self.answers) == len(self.questions): self.submit_btn.setEnabled(True)
   
    def record_answer(self, answer_text):
        """Record answers when selected"""
        for answer in self.answers:
            if self.num == answer['quest_num']:
                answer['answer'] = answer_text
                answer['mark'] = 1 if str(answer_text).strip().lower() == str(self.questions[self.num]['correct_option']).lower() else 0
                return
        
         #### If the question has not been answered before, do this #######    
        self.answers.append({
            "quest_num": self.num,
            "answer": answer_text,
            "mark": 1 if str(answer_text).strip().lower() == str(self.questions[self.num]['correct_option']).lower() else 0
        })
        return
            
    def submit_quiz(self):
        """Submit at the end of the quiz"""
        self.clear_layout(self.grid)
        for answer in self.answers:
            if answer['mark'] == 1: self.score_counter += 1
        self.name_label = QLabel(self.user_name, self)
        self.name_label.setObjectName("name_label")
        self.score = QLabel(f"You score {self.score_counter}/{len(self.questions)}")
        self.score_percent = QLabel(f"{self.score_counter/len(self.questions)*100:.2f} %")
        
        self.menu = QPushButton("Main Menu", self)
        self.menu.setFixedWidth(100)
        self.menu.clicked.connect(self.main_menu) 
            
        self.retake = QPushButton("Retake", self)
        self.retake.setFixedWidth(100)
        self.retake.clicked.connect(self.retake_quiz)     
        
        self.grid = QGridLayout()
        
        self.grid.addWidget(self.name_label, 1, 0, Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.score, 2, 0, Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.score_percent, 3, 0, Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.menu, 7, 0, Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(self.retake, 7, 0, Qt.AlignmentFlag.AlignRight)
        
        self.grid.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.setStyleSheet("""
            QLabel {
                font-style: Arial;
                margin: 10px;
                font-size: 32px;
            }
            QPushButton {
                font-style: Arial;
                padding: 10px;
                margin-top: 32px;
                font-size: 16px;
                border: 1px solid black;
                border-radius: 15px;
                background-color: rgb(220, 220, 220)
            }
            QPushButton::hover {
                background-color: transparent;
            }
                           """)
        
        self.widget = QWidget()
        self.widget.setLayout(self.grid)
        self.setCentralWidget(self.widget)
        
    def retake_quiz(self):        
        # Reset all params for new Quiz
        self.answers = []
        self.num = 0
        self.score_counter = 0
        self.get_quiz()
        
    def next_question(self):
       """Go to next question"""
       self.num += 1
       self.get_quiz()
       
    def prev_question(self):
        """Get Previous Question"""
        self.num -= 1
        self.get_quiz()
        
    def clear_layout(self, layout):
        # layout = self.grid
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                self.widget = item.widget()
                
                if self.widget is not None:
                    self.widget.deleteLater()
                    self.widget = None
                elif item.layout() is not None:
                    self.clear_layout(item.layout())
    
    def set_question(self):
        """Add question to question bank"""
        self.clear_layout(self.grid)
        self.grid = QGridLayout(self)
        
        # Title Label
        self.name_label = QLabel("ADD QUESTION", self)
        self.name_label.setObjectName("name_label")
        self.grid.addWidget(self.name_label, 1, 0, Qt.AlignmentFlag.AlignCenter)
        
        # Question Label
        self.question_label = QLabel("Question: ", self)
        self.question_label.setContentsMargins(0, 0, 0, 0)
        self.grid.addWidget(self.question_label, 2, 0, Qt.AlignmentFlag.AlignLeft)
        
        # Question Input
        self.question = QLineEdit()
        self.question.setFixedWidth(400)
        self.question.setPlaceholderText("Enter your question...")
        self.question.setContentsMargins(75, 15, 0, 0)
        self.grid.addWidget(self.question, 2, 0, Qt.AlignmentFlag.AlignLeft)
        
        # Option Label
        self.option_label = QLabel("Options: ", self)
        # self.option_label.setFixedSize(50, 30)
        self.grid.addWidget(self.option_label, 3, 0, Qt.AlignmentFlag.AlignLeft)
        self.option_label.setContentsMargins(0, 20, 0, 10)
        
        # Option Inputs
        # Creates 4 options
        for i in range(4):
            # Option letters
            self.letters[i] = QLabel(f"{self.letters[i]}: ", self)
            self.letters[i].setFixedWidth(100)
            self.grid.addWidget(self.letters[i], i+4, 0, Qt. AlignmentFlag.AlignLeft)
            
            # Option inputs
            self.letters[i] = QLineEdit(self)
            self.letters[i].setFixedWidth(400)
            self.letters[i].setPlaceholderText("Enter Option")
            self.letters[i].setStyleSheet("margin-left: 25px; margin-top: 15px;")
            self.grid.addWidget(self.letters[i], i + 4, 0, Qt.AlignmentFlag.AlignLeft)
        
        # Correct Answer Label   
        self.answer_label = QLabel("Correct Answer: ")
        self.grid.addWidget(self.answer_label, 10, 0, Qt.AlignmentFlag.AlignLeft)
        
        # Correct answer input
        self.correct_answer = QLineEdit(self)
        self.correct_answer.setFixedWidth(400)
        self.correct_answer.setPlaceholderText("Enter correct answer in full...")
        self.correct_answer.setStyleSheet("margin-left: 120px; margin-top: 15px;")
        self.grid.addWidget(self.correct_answer, 10, 0, Qt.AlignmentFlag.AlignLeft)
        
        # Add question button
        self.add_question = QPushButton("Add Question", self)
        self.add_question.setFixedWidth(200)
        self.add_question.clicked.connect(self.add_question_to_bank)
        self.grid.addWidget(self.add_question, 12, 0, Qt.AlignmentFlag.AlignCenter)
        
        self.setStyleSheet("""
               QLabel {
                    font-size: 16px;
                    font-family: Arial;
                    margin-top: 20px;
               }
               QLabel#name_label {
                   margin-bottom: 30px;
                   font-size: 32px;
               }
               QLineEdit {
                   font-size: 16px;
                   border:none;
                   background-color: transparent;
                   border-bottom: 1px solid;                   
               }
               QPushButton {
                   font-size: 16px;
                   margin: 20px;
                   padding: 10px;
                   border: 1px solid black;
                   border-radius: 20px;
                   background-color: rgb(220, 220, 220)
               }
               QPushButton::hover {
                   background-color: transparent;
               }
                           
                           """)
        
        
        self.grid.setContentsMargins(10, 10, 10, 100)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.widget = QWidget()
        self.widget.setLayout(self.grid)
        self.setCentralWidget(self.widget)
    
    def main_menu(self):
        self.init_UI()
              
    # Add question to bank
    def add_question_to_bank(self):
        """Add question to question bank"""
        # Checks the input and then saves it to question bank
        if self.question.text() == "":return QMessageBox.critical(None, "Error", "You have not entered any question!")
        elif self.correct_answer.text() == "": return QMessageBox.critical(None, "Error", "You have not entered the correct answer!")
        """Add question to bank"""
        self.questions.append({"question": self.question.text(), "options":[self.letters[i].text() for i in range(4) if self.letters[i].text() != ""], "correct_option": self.correct_answer.text()})
        
        data_string = json.dumps(self.data, indent=4)
        with open(self.file_path, 'w') as file:
            file.write(data_string)
            
        self.clear_layout(self.grid)
        self.init_UI()
            
    # Get Answer of User Input  
    def eventFilter(self, watched, event):
        """Get input of text type and record"""
        if watched == self.input_answer and len(self.input_answer.text()) > 0 and event.type() == QEvent.Type.FocusOut: self.record_answer(self.input_answer.text())
        #Enable submit button after attempting all questions
        if not self.submit_btn.isEnabled() and len(self.answers) == len(self.questions): self.submit_btn.setEnabled(True)
        return super().eventFilter(watched, event)

app = QApplication(sys.argv)    
window = mainWindow()
window.show()
sys.exit(app.exec())
