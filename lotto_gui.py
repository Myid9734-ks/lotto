import random
from sympy import Range, im, true
import sqlite3
import sys 
from PyQt5.QtWidgets import * 
from PyQt5 import uic , QtGui
import requests

form_class = uic.loadUiType("ma.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.check_btn.clicked.connect(self.odd_num)
        self.start_btn.clicked.connect(self.new_uum)
        
        self.all_num=[]
        self.num_arr = []
        self.zero_num = 0
        
        
        
        
# 과거 회차에서 넘버 불러와서 DB에 저장하기
        conn = sqlite3.connect ('lotto_db.db')
        c = conn.cursor()
        sql = 'select no from lotto order by no desc'
        a = c.execute(sql)
        zero_num_list = list(a.fetchone())
        zero_num = int(zero_num_list[0])
        conn.close()

        self.num_arr = []
        try:
            for num in range(zero_num+1, zero_num+1000):
                params ={'method' : 'getLottoNumber', 'drwNo' : num}
                request = requests.get('https://www.dhlottery.co.kr/common.do', params=params)
                response = request.json()
                # print(f"{response['drwNo']}회차 저장완료")
                
                a = {response['drwNo']}
                # print(a,'sssssssssssssssssss')
                for i in range(1, 7):
                    self.num_arr.append(response['drwtNo' + str(i)])
                conn = sqlite3.connect ('lotto_db.db')
                c = conn.cursor()
                sql = 'insert into lotto(no, no_1, no_2, no_3, no_4, no_5, no_6) values({},{},{},{},{},{},{})'.format(response['drwNo'], self.num_arr[0], self.num_arr[1], self.num_arr[2], self.num_arr[3], self.num_arr[4], self.num_arr[5])
                c.execute(sql)
                conn.commit()
                self.num_arr = []
                
            conn.close()
        except:
            self.statusBar().showMessage(f"{zero_num} 회차까지 불러오기 완료")
            
            
    
    
    
        
    def odd_num(self): # 이전회차 불러오기
        buttonReply = QMessageBox.question(self, '신중하게 결정', "500원?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.No:
            QMessageBox.about(self, '경고!!!!','꺼져!!!')
        else :
            self.new_num.clear()
        # text, ok = QInputDialog.getText(self, 'input dialog', 'Plald')
            self.test.clear()
            count = 1
            conn = sqlite3.connect ('lotto_db.db')
            c = conn.cursor()
            
            sql = 'select * from lotto order by no desc'
            a = c.execute(sql)
            zero_num_list = list(a.fetchall())
            for i in zero_num_list:
                a = '{}회차 : {}, {}, {}, {}, {}, {} '.format(i[0], i[1], i[2], i[3], i[4], i[5], i[6])
                self.test.appendPlainText(a)
                self.test.appendPlainText('--------------------------')
                count += 1
            self.test.moveCursor(QtGui.QTextCursor.Start)
            
            count = 0
            
            sql = 'SELECT no_1, no_2,no_3,no_4,no_5,no_6 FROM lotto ORDER by no DESC'
            a = c.execute(sql)
            zero_num_list = list(a.fetchall())
            
            
            # self.my_lotto_numbers = [46,46,46,46,46,46]
            no = []
            count = 0
            for i in (self.my_lotto_numbers):
                if type(i) == int:
                    # print(self.my_lotto_numbers)
                    for i in zero_num_list:
                        old_set = set(i) & set(self.my_lotto_numbers)
                        # print(old_set)                    
                        if len(old_set) == 3:
                            no.append('5등')
                        elif len(old_set) == 4:
                            no.append('4등')
                        elif len(old_set) == 5:
                            no.append('3등')
                        elif len(old_set) == 6:
                            no.append('1등')
                        else:
                            no.append('꽝')
                    count += 1
                    a = '{}번 : {}, {}, {}, {}, {}, {} '.format(count, self.my_lotto_numbers[0], self.my_lotto_numbers[1], self.my_lotto_numbers[2], self.my_lotto_numbers[3], self.my_lotto_numbers[4], self.my_lotto_numbers[5])
                    self.new_num.appendPlainText(a)
                    a = '5등 {}회, 4등 {}회, 3등 {}회, 1등 {}회, 꽝 {}회'.format(no.count('5등'), no.count('4등'), no.count('3등'), no.count('1등'), no.count('꽝'))
                    self.new_num.appendPlainText(a)
                    self.new_num.appendPlainText('-------------------------------------')
                    self.new_num.appendPlainText(' ')
                    break
                else:
                    for x in zero_num_list:
                        old_set = set(i) & set(x)
                        if len(old_set) == 3:
                            no.append('5등')
                        elif len(old_set) == 4:
                            no.append('4등')
                        elif len(old_set) == 5:
                            no.append('3등')
                        elif len(old_set) == 6:
                            no.append('1등')
                        else:
                            no.append('꽝')
                    count += 1
                    a = '{}번 : {}, {}, {}, {}, {}, {} '.format(count, i[0], i[1], i[2], i[3], i[4], i[5])
                    self.new_num.appendPlainText(a)
                    a = '5등 {}회, 4등 {}회, 3등 {}회, 1등 {}회, 꽝 {}회'.format(no.count('5등'), no.count('4등'), no.count('3등'), no.count('1등'), no.count('꽝'))
                    self.new_num.appendPlainText(a)
                    self.new_num.appendPlainText('-------------------------------------')
                    self.new_num.appendPlainText(' ')
                    no = []
            self.statusBar().showMessage(f"예전 회차와 비교완료")
            
                             
                        
            
            
        
        
        
    def new_uum(self):
        count_num_text = self.count_num.toPlainText()
        try:
            count_num_text = int(count_num_text)
        except:
            pass
        self.count_num.clear()
        self.new_num.clear()
        self.test.clear()
        luck_number = []
        self.my_lotto_numbers = []
        count_num = 0
        # while len(self.my_lotto_numbers) < int(count_num_text): # 5장의 번호를 수집
        if type(count_num_text) == int:
            while count_num <  int(count_num_text): # 5장의 번호를 수집
                list_of_numbers = list(range(1, 46)) # 1~45까지 범위 지정
                random.shuffle(list_of_numbers) # 임의이 정렬로 숫자 썩기
                numbers = list_of_numbers[:6]  # 첫번째부터 6번째까지 숫자 뽑기
                numbers.sort()
                
                self.my_lotto_numbers.append(numbers)
                
                count_num += 1
                # count_matchiong_numbers(numbers)
                # my_lotto_numbers=[]
            count = 1
            for i in self.my_lotto_numbers:
                a = '{}번 : {}, {}, {}, {}, {}, {} '.format(count, i[0], i[1], i[2], i[3], i[4], i[5])
                self.new_num.appendPlainText(a)
                self.new_num.appendPlainText('--------------------------')
                count += 1
            self.check_btn.setEnabled(True)
            self.statusBar().showMessage(f"{count_num_text}회 생성완료")
        else:
            self.statusBar().showMessage("숫자만 입력하세요")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()