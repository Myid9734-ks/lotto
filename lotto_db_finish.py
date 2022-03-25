import requests
import sqlite3
import random
from slacker import Slacker
import time
slack = Slacker('xoxb-1630693147620-1621444099845-ogZMvoy5ozRdMxxMz4311CP7')

real_number = []
my_lotto_numbers = []
luck_number = []


now = time.localtime()
nowTime = '%02d%02d%02d' % (now.tm_hour, now.tm_min, now.tm_sec)
nowTime_1 = '%02d%s %02d%s %02d%s' % (now.tm_hour,'시', now.tm_min,'분', now.tm_sec,'초')
nowDate = '%04d%s %02d%s %02d%s' % (now.tm_year,'년', now.tm_mon, '월', now.tm_mday, '일')
days = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']


# 과거 회차에서 넘버 불러와서 DB에 저장하기
conn = sqlite3.connect ('lotto_db.db')
c = conn.cursor()
sql = 'select no from lotto order by no desc'
a = c.execute(sql)
zero_num_list = list(a.fetchone())
zero_num = int(zero_num_list[0])
print(f'마지막으로 저장된 회차는 {zero_num} 입니다.')
conn.close()

# for i in a:
#     print(i[0])
# print('*********************************')
# print('----------------------------------------')
# print(a.fetchall())
# # b = a.fetchmany(size=10)
num_arr = []

try:
    for num in range(zero_num+1, zero_num+1000):
        params ={'method' : 'getLottoNumber', 'drwNo' : num}
        request = requests.get('https://www.dhlottery.co.kr/common.do', params=params)
        response = request.json()
        print(f"{response['drwNo']}회차 저장완료")
        print('-----------------')
        for i in range(1, 7):
            num_arr.append(response['drwtNo' + str(i)])
        conn = sqlite3.connect ('lotto_db.db')
        c = conn.cursor()
        sql = 'insert into lotto(no, no_1, no_2, no_3, no_4, no_5, no_6) values({},{},{},{},{},{},{})'.format(response['drwNo'], num_arr[0], num_arr[1], num_arr[2], num_arr[3], num_arr[4], num_arr[5])
        c.execute(sql)
        conn.commit()
        num_arr = []
    conn.close()
except:
    print('*******************')
    print('모든 회차 저장완료')






# 임의의 숫자 뽑기
conn = sqlite3.connect ('lotto_db.db')
c = conn.cursor()
sql = 'select no_1, no_2, no_3, no_4, no_5, no_6 from lotto'
a = c.execute(sql)
old_num = a.fetchall()

def count_matchiong_numbers(list_2):
    for i in old_num:
        same_number = list(set(i).intersection(list_2))
        if len(same_number) < 2:
            if list_2 not in luck_number:
                luck_number.append(list_2)
    
            
while len(luck_number) < 10: # 5장의 번호를 수집
    list_of_numbers = list(range(1, 46)) # 1~45까지 범위 지정
    random.shuffle(list_of_numbers) # 임의이 정렬로 숫자 썩기
    numbers = list_of_numbers[:6]  # 첫번째부터 6번째까지 숫자 뽑기
    my_lotto_numbers.append(numbers)
    count_matchiong_numbers(numbers)
    print(numbers,'-----------------')
    my_lotto_numbers=[]


for i in luck_number:
    i.sort()
    print(i)

# 슬랙 메세지로 전송
zero_num = int(zero_num) + 1
count1 = 1
slack.chat.post_message('#lotto','{}회자 예상번호----{}'.format(zero_num, nowDate))
for i in luck_number:
    slack.chat.post_message('#lotto','No_{}: {}'.format(count1,sorted(i)))
    count1 += 1
slack.chat.post_message('#lotto','------------------------------------')
print(zero_num)