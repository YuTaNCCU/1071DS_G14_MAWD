import feasible_test as ft
import feasible_test_with_print_error as fterr
import random
import functions as func
import pandas as pd

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

all_course = list(pd.read_csv('data/course.csv')['course code'].astype(str))

def get_schedule():
    blank_schedule = ['']*45
    while(True):
        if(ft.feasible_test(blank_schedule)):
            # print("------ 生成初始課表{}成功! 得分為: {} ------".format(i,get_score(blank_schedule)))
            # print(blank_schedule)
            return blank_schedule
        else:
            blank_schedule = ['']*45
            for course in all_course:
                while(True):
                    random_number = random.randint(0,len(blank_schedule)-1)
                    if blank_schedule[random_number] == "":
                        blank_schedule[random_number] = course
                        break
                    else:
                        pass