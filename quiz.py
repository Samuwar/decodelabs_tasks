####### QUIZ APP ##########
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QInputDialog, QLineEdit, QGridLayout, QRadioButton, QHBoxLayout
from PyQt6.QtCore import Qt, QRect

class mainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Quiz App")
        self.setGeometry(100, 50, 800, 800)
        self.name_label = QLabel("Name: ", self)
        self.name_label.setFixedSize(100, 40)
        self.input_box = QLineEdit(self)
        self.input_box.setFixedSize(200, 40)
        self.submit_btn = QPushButton("Submit Text", self)
        self.submit_btn.setFixedSize(100, 40)
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        self.num = 0
        self.user_name = "Abimbola"
        self.answers = []
        self.score_counter = 0
        self.questions = [
                        {
                            "question": "What is your name",
                            "options": ["Abimbola", "Ibrahim", "David"],
                            "correct_option": "Abimbola"
                        },
                        {
                            "question": "When did Nigeria gain her independence?",
                            "options": [1900, 1956, 1960, 1982],
                            "correct_option": 1960
                        },
                        {
                            "question": "Under whose regime was mobile phone introduced to Nigeria?",
                            "options": ["President Muhammad Buhari", "President Olusegun Obasanjo", "President Ahmed Tinubu", "President Murtala Muhammed"],
                            "correct_option": "President Olusegun Obasanjo"
                        }
                    ]
        
        self.init_UI()
        
    def init_UI(self):
        self.grid = QGridLayout(self)

        self.name_label.setStyleSheet("font-size: 16px")
        
        self.input_box.setPlaceholderText("Enter your name")
        self.input_box.setStyleSheet("font-size:16px; outline:none")
        
        self.submit_btn.setStyleSheet("color:blue; font-size:16px; width:fit-content;")
        self.submit_btn.clicked.connect(self.get_quiz)
        
        ##### SET BASE ROWS AND COLUMNS #########
        self.empty_label = QLabel("", self)
        self.grid.addWidget(self.empty_label, 10, 6)
        
        self.setStyleSheet("""
                QPushButton{
                    margin-top: 10px;
                    padding: 5px;
                    border: 1px solid;
                    border-radius: 15px;
                }
                QLineEdit {
                    margin-left: 0;
                    padding-left: 5px;
                    border: none;
                    border-bottom: 1px solid;
                    background-color: transparent;
                }
                           """)
        self.grid.addWidget(self.name_label, 4, 0, 5, 3, Qt.AlignmentFlag.AlignRight)
        self.grid.addWidget(self.input_box, 4, 3, 5, 4, Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(self.submit_btn, 4, 3, 6, 1)
        
        self.widget = QWidget()
        self.widget.setLayout(self.grid)
        self.setCentralWidget(self.widget)
        
    def get_quiz(self):
        self.clear_layout(self.grid)
        self.grid = QGridLayout(self)
        self.hlayout = QHBoxLayout()
        # self.user_name = self.input_box.text()
        self.name_label = QLabel(self.user_name, self)
        self.name_label.setObjectName("name_label")
        self.grid.addWidget(self.name_label, 1, 4, 1, 3, Qt.AlignmentFlag.AlignCenter)
        self.question_label = QLabel("",self)
        self.question_label.setWordWrap(True)
        self.question_label.setFixedSize(500, 100)
        
        question = {}
        try: question = self.questions[self.num]
        except IndexError: self.error = QLabel("No Question Found")
         
        self.answered_counter = 0
        if question: 
            self.question_label.setText(f"<b>Question:</b> {question['question']}")
            self.grid.addWidget(self.question_label, 3, 5, Qt.AlignmentFlag.AlignLeft)
            self.question_label.setObjectName("question_label")
            self.option_label = QLabel(f"<b>Options: </b>")
            self.grid.addWidget(self.option_label, 4, 5)
            for index, option in enumerate(question['options']):
                self.letters[index] = QRadioButton(str(option), self)
                for answer in self.answers:
                    if self.num == answer['quest_num'] and answer['answer'] == str(option): self.letters[index].setChecked(True)
                self.letters[index].toggled.connect(self.record_answer)
                self.grid.addWidget(self.letters[index], index + 5, 5, Qt.AlignmentFlag.AlignLeft)
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
        self.submit_btn.setDisabled(True)
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
                           
                           """)
        
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.widget = QWidget()
        self.widget.setLayout(self.grid)
        self.setCentralWidget(self.widget)

  
    def record_answer(self):
        response = self.sender()
        num = self.num
        if response.isChecked():
            for answer in self.answers:
                if num == answer['quest_num']:
                    answer['answer'] = response.text()
                    if str(response.text()).lower() == str(self.questions[num]['correct_option']).lower(): answer['mark'] = 1
                    else: answer['mark'] = 0
                    
                    if not self.submit_btn.isEnabled() and len(self.answers) == len(self.questions): self.submit_btn.setDisabled(False)
                    
                    return print(self.answers)
                
            self.answers.append({
                "quest_num": num,
                "answer": response.text(),
                "mark": 1 if str(response.text()).lower() == str(self.questions[num]['correct_option']).lower() else 0
            })
            if not self.submit_btn.isEnabled() and len(self.answers) == len(self.questions): self.submit_btn.setDisabled(False)
        return print(self.answers)
            
    def submit_quiz(self):
        self.clear_layout(self.grid)
        for answer in self.answers:
            if answer['mark'] == 1: self.score_counter += 1
        self.name_label = QLabel(self.user_name, self)
        self.score = QLabel(f"Your score is {self.score_counter}/{len(self.questions)}")
        self.score_percent = QLabel(f"{self.score_counter/len(self.questions)*100:.2f} %")
        
        self.grid = QGridLayout()
        
        self.grid.addWidget(self.name_label, 2, 3)
        self.grid.addWidget(self.score, 4, 3)
        self.grid.addWidget(self.score_percent, 5, 3)
        
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.widget = QWidget()
        self.widget.setLayout(self.grid)
        self.setCentralWidget(self.widget)
        
            
             
            
        
    def next_question(self):
       """Go to next question"""
       
       self.num += 1
       self.get_quiz()
       
    def prev_question(self):
        self.num -= 1
        self.get_quiz()
            
        
    def get_input_text(self):
        user_text = self.input_box.text()
        
        print(f"Your name is {user_text}")
        
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
        
    def button_clicked(self):
        print('click')
        
        text, ok = QInputDialog.getText(self, "Input Box Title", "Enter Your Name")
        
        if ok and text:
            print(f"User entered: {text}")
        

app = QApplication(sys.argv)    
window = mainWindow()
window.show()
sys.exit(app.exec())
    

# user_name = input("Enter Your Name: ")
# counter = 0
# if input("What is the capital of Nigeria? ").lower().strip() == 'lagos': counter += 1
# if input("When did Nigeria gain her independence? ").lower().strip() == '1960': counter += 1
# if int(input("Under whose regime was mobile phone introduced to Nigeria? \n1. President Muhammad Buhari \n2. President Obansanjo \n3. President Ahmed Tinubu \n4. President Murtala Muhammed \nSelect the right option: ")) == 2: counter += 1

# print(f"Your total score is: {counter}")