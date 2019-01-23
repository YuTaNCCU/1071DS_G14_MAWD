# In[] 
import pandas as pd
import numpy as np
import random 
#讀取
courseDetail = pd.read_csv('data/course.csv')[['course code', 'Number of students', 'instructor']]
teacherDetail= pd.read_csv('data/instructor.csv')[['i_no', 'instructor name']]
courseDetail['course code']=courseDetail['course code'].astype(str)
RoomDetail = pd.read_csv('data/classroom.csv')[['classroom', 'cr_capacity']]
totalCourseNum=len(courseDetail['course code'])
cNum = len(courseDetail['instructor']) 	#課程總數
tNum = len(teacherDetail['i_no'])+1		#老師總數
#variables
roomNum=3 #教室數量
weekdays=5 #上課日子
dailyParts=3 #parts=將一天劃分為[早上、下午、晚上]
period=weekdays*dailyParts #15 一個weekdays中，不分教室的區塊總數
session=roomNum*weekdays*dailyParts #45 一個weekdays中，空教室的總數(一維陣列的長度)
k=weekdays*roomNum #15 [早上、下午、晚上] 一個part中的session數(索引調整參數)

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

#生成空的list[list]
def init_list_of_objects(size):
    list_of_objects = list()
    for i in range(0,size):
        list_of_objects.append( list() ) #different object reference each time
    return list_of_objects


def generate(courseDetail, tNum, cNum, period):
	#initial empty schedule 預設為空直
	schedule=[]
	for i in range(session):
	    schedule.append('')

	courseDetail=courseDetail.drop(columns="Number of students") 
	courseDetail = courseDetail[['instructor', 'course code']]

	instructorReport = courseDetail.groupby(['instructor']).agg({"course code":'count'}).sort_values(['course code'],ascending=False).copy()
	instructorReport = instructorReport.reset_index()
	instructorReport['instructor']=instructorReport['instructor'].astype(str)

	#老師排入空課表的優先順序
	y=np.array(instructorReport['instructor'])
	y=y.tolist()
	#['9', '5', '1', '7', '6', '4', '8', '3', '10']

	teacher=init_list_of_objects(tNum)    		#空的教師列表
	for x in range(cNum):
		key= courseDetail['instructor'][x]		#key
		value= courseDetail['course code'][x]	#value
		teacher[key].append(value)  			#各教師的授課列表

	#每個教師的排課順序亂數
	for key in range(len(teacher)):
		if teacher[key]!=[]:
			teacher[key]=random.sample(teacher[key], len(teacher[key]))
	#合併成要排入的課程list
	query=[]
	for order in y:
		o=int(order)
		query=query+teacher[o]

	#query照順序排入課表
	querylen=len(query)
	index=0
	classroom=1
	for x in range(3):
		for y in range(period):
			#填完break
			if index==querylen:
				break
			#填入，下一個query
			schedule[x+3*y]=query[index]
			index=index+1
		if index==querylen:
			break
	return schedule

#print("Random Initial Solution: ", generate(courseDetail, tNum, cNum, period))
#30['306008001', '307942001', '', '306525001', '356808001', '', '307851001', '306736001', '', '307867001', '307873001', '', '356019001', '356388001', '', '356387001', '356395001', '', '356813001', '306016022', '', '306000001', '307034001', '', '306737001', '356389001', '', '307857001', '306016002', '', '356425001', '307901001', '', '356461001', '307035001', '', '356822001', '307932001', '', '306016012', '356564001', '', '307870001', '306050011', '']
#33['306008001', '307870001', '307932001', '306525001', '307942001', '356564001', '307851001', '356808001', '306050011', '307867001', '306016022', '', '356019001', '307034001', '', '356387001', '356389001', '', '356813001', '356813002', '', '356813004', '306736001', '', '306000001', '307873001', '', '306737001', '356388001', '', '307857001', '356395001', '', '356425001', '306016002', '', '356461001', '307901001', '', '356822001', '356813003', '', '306016012', '307035001', '']