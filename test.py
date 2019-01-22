# In[] 
import pandas as pd
import numpy as np
#讀取
courseDetail = pd.read_csv('data/course.csv')[['course code', 'Number of students', 'instructor']]
teacherDetail= pd.read_csv('data/instructor.csv')[['i_no', 'instructor name']]
courseDetail['course code']=courseDetail['course code'].astype(str)
RoomDetail = pd.read_csv('data/classroom.csv')[['classroom', 'cr_capacity']]

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

#initial empty schedule 預設為空直
schedule=[]

for i in range(session):
    schedule.append('')
#生成空的list[list]
def init_list_of_objects(size):
    list_of_objects = list()
    for i in range(0,size):
        list_of_objects.append( list() ) #different object reference each time
    return list_of_objects

# testing data

schedule=['306000001','','306008001','','','306016002','356425001','','306016012','307873001','','307867001','307942001','','307870001',
 '306016022','307857001','306050011','356387001','356388001','307851001','306525001','','307035001','306736001','356395001','307034001','356461001','','306737001',
'307932001','','356822001','','356389001','356019001','356564001','','307901001','356813001','','356808001','','','']
#print(courseDetail)#course code, Number of students, instructor
courseDetail=courseDetail.drop(columns="Number of students") 
#print(courseDetail)#course code, instructor
courseDetail = courseDetail[['instructor', 'course code']]
print(courseDetail)

instructorReport = courseDetail.groupby(['instructor']).agg({"course code":'count'}).sort_values(['course code'],ascending=False).copy()
instructorReport = instructorReport.reset_index()
instructorReport['instructor']=instructorReport['instructor'].astype(str)
#print(instructorReport) #照授課數排的instructor, sum(course)
#老師排入空課表的優先順序 轉換成list
y=np.array(instructorReport['instructor'])
y=y.tolist()
#teacherNum=len(y)
#老師排入空課表的優先順序['9', '5', '1', '7', '6', '4', '8', '3', '10']


teacher=init_list_of_objects(tNum)    #空的教師列表
for x in range(cNum):
	key= courseDetail['instructor'][x]#key
	value= courseDetail['course code'][x]#value
	print(key, value)
	teacher[key].append(value)
print(teacher) #各教師的授課列表

#轉換成字典
#x=courseDetail.to_dict('records')
#print(x['instructor'])
#[{'instructor': 5, 'course code': '306000001'}, {'instructor': 9, 'course code': '306008001'}, {'instructor': 4, 'course code': '306016002'}, {'instructor': 1, 'course code': '306016012'}, {'instructor': 6, 'course code': '306016022'}, {'instructor': 10, 'course code': '306050011'}, {'instructor': 9, 'course code': '306525001'}, {'instructor': 7, 'course code': '306736001'}, {'instructor': 5, 'course code': '306737001'}, {'instructor': 6, 'course code': '307034001'}, {'instructor': 8, 'course code': '307035001'}, {'instructor': 9, 'course code': '307851001'}, {'instructor': 5, 'course code': '307857001'}, {'instructor': 9, 'course code': '307867001'}, {'instructor': 1, 'course code': '307870001'}, {'instructor': 7, 'course code': '307873001'}, {'instructor': 4, 'course code': '307901001'}, {'instructor': 8, 'course code': '307932001'}, {'instructor': 1, 'course code': '307942001'}, {'instructor': 9, 'course code': '356019001'}, {'instructor': 9, 'course code': '356387001'}, {'instructor': 7, 'course code': '356388001'}, {'instructor': 6, 'course code': '356389001'}, {'instructor': 7, 'course code': '356395001'}, {'instructor': 5, 'course code': '356425001'}, {'instructor': 5, 'course code': '356461001'}, {'instructor': 3, 'course code': '356564001'}, {'instructor': 1, 'course code': '356808001'}, {'instructor': 5, 'course code': '356822001'}, {'instructor': 9, 'course code': '356813001'}]



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