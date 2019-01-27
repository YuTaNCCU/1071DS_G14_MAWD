import random
import pandas as pd
import numpy as np
import time
import functions as func

#讀取courseDetail
courseDetail = pd.read_csv('data/course.csv')[['course code', 'Number of students', 'instructor']]
courseDetail['course code']=courseDetail['course code'].astype(str)
RoomDetail = pd.read_csv('data/classroom.csv')[['classroom', 'cr_capacity']]
teacherDetail= pd.read_csv('data/instructor.csv')[['i_no', 'instructor name']]
cNum = len(courseDetail['instructor']) 	#課程總數
tNum = len(teacherDetail['i_no'])+1		#老師總數

#variables
roomNum=3 #教室數量
weekdays=5 #上課日子
dailyParts=3 #parts=將一天劃分為[早上、下午、晚上]
period=weekdays*dailyParts #15 一個weekdays中，不分教室的區塊總數
session=roomNum*weekdays*dailyParts #45 一個weekdays中，空教室的總數(一維陣列的長度)
k=weekdays*roomNum #15 [早上、下午、晚上] 一個part中的session數(索引調整參數)
totalCourseNum=30

def get_score(schedule):
    return func.ObjFun(schedule,courseDetail, roomNum, k, RoomDetail, session, period, totalCourseNum)

def cross(schedule_1,schedule_2):
    while(True):
        # select cross index
        cross_index1 = random.randint(0, len(schedule_1)-1)
        cross_index2 = random.randint(0, len(schedule_2)-1)
        while(cross_index1 >= cross_index2):
            cross_index1 = random.randint(0, len(schedule_1)-1)
            cross_index2 = random.randint(0, len(schedule_2)-1)

        # make new schedule
        new_schedule = schedule_1[0: cross_index1] + schedule_2[cross_index1 : cross_index2] + schedule_1[cross_index2 : 45]  

        # origin
        # 2 8 | 6 4 5 | 7 1 3
        # 8 7 | 2 1 3 | 4 6 5

        # cross finish
        # 2 8 | 2 1 3 | 7 1 3
        # 8 7 | 6 4 5 | 4 6 5 

        # fix (ex: 2去換回"自己"原本有的6)
        # 6 8 | 2 1 3 | 7 4 5
        # 8 7 | 6 4 5 | 4 6 5

        for i in range(cross_index1,cross_index2): #cross範圍
            data = new_schedule[i] # i位置資料 (ex:此處是2)
            data_index = schedule_1.index(data) #此筆資料位於原schedule的什麼位置 (ex:此處2找到位於為schedule "0的位置" )
            new_schedule[data_index] = schedule_1[i] # new_schedule的該位置換成cross對應字串 (ex:此處原"0的位置" 2換成 "i對應位置的6" )

        if func.feasible_test(new_schedule):  
#             print("找到解!")
            return new_schedule

        # ------------------------------------------------------------------#
        # make new schedule reverse
        new_schedule = schedule_2[0: cross_index1] + schedule_1[cross_index1 : cross_index2] + schedule_2[cross_index2 : 45]  

        for i in range(cross_index1,cross_index2): #cross範圍
            data = new_schedule[i] # i位置資料 (ex:此處是2)
            data_index = schedule_2.index(data) #此筆資料位於原schedule的什麼位置 (ex:此處2找到位於為schedule "0的位置" )
            new_schedule[data_index] = schedule_2[i] # new_schedule的該位置換成cross對應字串 (ex:此處原"0的位置" 2換成 "i對應位置的6" )

        if func.feasible_test(new_schedule):  
#             print("找到解!")
            return new_schedule
        # ------------------------------------------------------------------#

def one_generation(schedule1,schedule2):
    result = False
    stop_flag= False
    gene_pool = []
    gene_score = []
    result_count = 0

    while(result_count < 100):
        new_schedule = cross(schedule1,schedule2)
        result_count += 1
        gene_pool.append(new_schedule)
        gene_score.append(float(get_score(new_schedule)))
#         print("在此子代中找到第 {} 個解, 得分為: {}".format(result_count,get_score(new_schedule)))
  
    gene_score_sorted = sorted(gene_score, reverse=True)
    
    next_gen1 = gene_pool[gene_score.index(gene_score_sorted[0])]    
    
    if max(gene_score_sorted) == min(gene_score_sorted):
        stop_flag = True
        next_gen2 = next_gen1 
    else:
        for score_data in gene_score_sorted:
            if score_data == max(gene_score_sorted):
                pass
            else:
                next_gen2 = gene_pool[gene_score.index(score_data)]
                break 
                
    return next_gen1,next_gen2,stop_flag


def get_one_ans():
    temp_schedule = func.get_schedule()
    temp_schedule2 = func.get_schedule()
    while(temp_schedule == temp_schedule2):
        temp_schedule2 = func.get_schedule()
        
    print("初始解1得分為: {}".format(get_score(temp_schedule)))
    print("初始解2得分為: {}".format(get_score(temp_schedule2)))

    delta = 0.0000001
    best_score = 0
    same_high_score_count = 0
    best_schedule= []
    stop_flag = False

    if get_score(temp_schedule2) > best_score:
        best_score = get_score(temp_schedule2)
        best_schedule = temp_schedule2

    next_gen1,next_gen2 = temp_schedule, temp_schedule2

    for i in range(1,1000):
        next_gen1,next_gen2,stop_flag = one_generation(next_gen1,next_gen2)
        if get_score(next_gen1) - best_score < delta:
            same_high_score_count += 1
        else:
            same_high_score_count = 0

        if stop_flag:
            break

        if same_high_score_count >= 10:
            break

        if get_score(next_gen1) > best_score:
            best_score = get_score(next_gen1)
            best_schedule = next_gen1
            
    print("---> 已找到最佳解，得分為：{}\n".format(best_score))
#     print(best_schedule)
    
    return best_schedule,best_score

def get_one_ans_print_details():
    temp_schedule = func.get_schedule()
    temp_schedule2 = func.get_schedule()
    while(temp_schedule == temp_schedule2):
        temp_schedule2 = func.get_schedule()

    delta = 0.0000001
    best_score = 0
    same_high_score_count = 0
    best_schedule= []
    stop_flag = False

    print("-----初始解-----")
    print("------初始解1------")
    print(temp_schedule)
    print(func.feasible_test(temp_schedule))
    print("得分為: {}".format(get_score(temp_schedule)))
    if get_score(temp_schedule) > best_score:
        best_score = get_score(temp_schedule)
        best_schedule = temp_schedule

    print("------初始解2------")
    print(temp_schedule2)    
    print(func.feasible_test(temp_schedule2))
    print("得分為: {}".format(get_score(temp_schedule2)))
    if get_score(temp_schedule2) > best_score:
        best_score = get_score(temp_schedule2)
        best_schedule = temp_schedule2

    next_gen1,next_gen2 = temp_schedule, temp_schedule2

    for i in range(1,1000):
        print("-----第{}子代-----".format(i))
        next_gen1,next_gen2,stop_flag = one_generation(next_gen1,next_gen2)
        print("此子代最高得分為: {}".format(get_score(next_gen1)))
        if get_score(next_gen1) - best_score < delta:
            same_high_score_count += 1
            print("*** 目前共第 {} 子代並未找到更加解! ***".format(same_high_score_count))
        else:
            same_high_score_count = 0

        if stop_flag:
            break

        if same_high_score_count >= 10:
            break

        if get_score(next_gen1) > best_score:
            best_score = get_score(next_gen1)
            best_schedule = next_gen1

    print("-----已找到最佳解，得分為：{}-----".format(best_score))    
    print(best_schedule)
    
    return best_schedule,best_score

best_schedule_list = []
best_score_list = []
calculate_time_list = []

for i in range(10):
    print("------ 第 {} 次找解 ------".format(i+1))
    start_time = time.time()
    best_schedule,best_score = get_one_ans()
#     best_schedule,best_score = get_one_ans_print_details()
    end_time = time.time()
    
    best_schedule_list.append(best_schedule)
    best_score_list.append(best_score)
    calculate_time_list.append(end_time - start_time)

print(best_score_list)
print(calculate_time_list)

# print(best_schedule_list[best_score.index(max(best_score))])
print(best_schedule_list[8])
