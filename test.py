# In[] 
import pandas as pd
import numpy as np
#讀取courseDetail
courseDetail = pd.read_csv('data/course.csv')[['course code', 'Number of students', 'instructor']]
#print(courseDetail)
courseDetail['course code']=courseDetail['course code'].astype(str)
#print(courseDetail)
RoomDetail = pd.read_csv('data/classroom.csv')[['classroom', 'cr_capacity']]
#print(RoomDetail)
#variables
roomNum=3 #教室數量
weekdays=5 #上課日子
dailyParts=3 #parts=將一天劃分為[早上、下午、晚上]
period=weekdays*dailyParts #15 一個weekdays中，不分教室的區塊總數
session=roomNum*weekdays*dailyParts #45 一個weekdays中，空教室的總數(一維陣列的長度)
k=weekdays*roomNum #15 [早上、下午、晚上] 一個part中的session數(索引調整參數)
totalCourseNum=30

#initial empty schedule 預設為空直
schedule=[]
for i in range(session):
    schedule.append('')
    
# testing data

schedule=['306000001','','306008001','','','306016002','356425001','','306016012','307873001','','307867001','307942001','','307870001',
 '306016022','307857001','306050011','356387001','356388001','307851001','306525001','','307035001','306736001','356395001','307034001','356461001','','306737001',
'307932001','','356822001','','356389001','356019001','356564001','','307901001','356813001','','356808001','','','']

schedule_Detail =  pd.DataFrame(schedule.copy(),  columns=['course code'])
schedule_Detail['course code']=schedule_Detail['course code'].astype(str)
schedule_Detail = pd.merge(schedule_Detail, courseDetail, how='left', on='course code')
print(type(courseDetail['instructor'][0]))
instructorReport = schedule_Detail.groupby(['instructor']).agg({"course code":'count'}).sort_values(['course code'],ascending=False).copy()
instructorReport = instructorReport.reset_index()
print(instructorReport)
x=instructorReport.to_dict('records')
print(x)

"""
1. 創建空的課表
2. 讀取所有課程資訊
3. 依照教師授課數sort教師名字與課程
假設有三個教授授課數分別為[A, B, C]=[3, 2, 6]
sort後順序為[C,A,B]=[6, 3, 2]
4. 優先取"授課數多的教師"的課程排入空課表中
先把C的6堂課排完才排A的3堂課，最後才排C的2堂課 
5. 用迴圈跑
優先順序：下午>早上>晚上、左至右(先忽略part，一律由早上開始排)
若跑完一輪，每個part中都有一堂課，才接著跑第二輪

"""