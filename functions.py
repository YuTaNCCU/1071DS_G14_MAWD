# In[] 參數設定
import pandas as pd
import numpy as np
#讀取courseDetail
courseDetail = pd.read_csv('data/course.csv')[['course code', 'Number of students', 'instructor']]
courseDetail['course code']=courseDetail['course code'].astype(str)
RoomDetail = pd.read_csv('data/classroom.csv')[['classroom', 'cr_capacity']]
teacherDetail= pd.read_csv('data/instructor.csv')[['i_no', 'instructor name']]
totalCourseNum=len(courseDetail['course code'])
tNum = len(teacherDetail['i_no'])+1     #老師總數

#variables
roomNum=3 #教室數量
weekdays=5 #上課日子
dailyParts=3 #parts=將一天劃分為[早上、下午、晚上]
period=weekdays*dailyParts #15 一個weekdays中，不分教室的區塊總數
session=roomNum*weekdays*dailyParts #45 一個weekdays中，空教室的總數(一維陣列的長度)
k=weekdays*roomNum #15 [早上、下午、晚上] 一個part中的session數(索引調整參數)

#initial schedule 預設為空直
schedule=[]
for i in range(session):
    schedule.append('')
#test.py    
#schedule=['306008001', '307942001', '', '306525001', '356808001', '', '307851001', '306736001', '', '307867001', '307873001', '', '356019001', '356388001', '', '356387001', '356395001', '', '356813001', '306016022', '', '306000001', '307034001', '', '306737001', '356389001', '', '307857001', '306016002', '', '356425001', '307901001', '', '356461001', '307035001', '', '356822001', '307932001', '', '306016012', '356564001', '', '307870001', '306050011', '']
#小麥的
#schedule=['306000001','','306008001','','','306016002','356425001','','306016012','307873001','','307867001','307942001','','307870001','306016022','307857001','306050011','356387001','356388001','307851001','306525001','','307035001','306736001','356395001','307034001','356461001','','306737001','307932001','','356822001','','356389001','356019001','356564001','','307901001','356813001','','356808001','','','']


# In[] #1 教授單日授課集中度(例如：老師一天從早上直接上課到晚上)
"""
Input: schedule(list), 含授課教師課程細節的courseDetail(dictionary)
Output: dailyConc(number) 0~1000分 : (number of sessions - number of days + 1)/ number of sessions
"""
def dailyConcentration(schedule, courseDetail, weekdays, dailyParts):
    #LEFT JOIN (schedule 與 courseDetail)
    schedule_Detail =  pd.DataFrame(schedule.copy(),  columns=['course code'])
    schedule_Detail['course code']=schedule_Detail['course code'].astype(str)
    schedule_Detail = pd.merge(schedule_Detail, courseDetail, how='left', on='course code')

    #生成45個session對應的Weekday
    WeekdayList=[1,2,3,4,5]
    WeekdayList=(WeekdayList * roomNum)
    WeekdayList.sort() #[1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5]
    WeekdayList=(WeekdayList * dailyParts)
    WeekdayList #[1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5]
    WeekdayList = pd.DataFrame({ 'weekday': WeekdayList})
    
    #schedule右邊新增一欄Weekday
    schedule_Detail = pd.concat([schedule_Detail, WeekdayList], axis=1)
    
    #計算各個老師的一週上課堂數、上課天數
    instructorReport = schedule_Detail.groupby(['instructor', 'weekday']).agg({"course code":'count'}).copy()
    instructorReport = instructorReport.reset_index()
    instructorReport['course code']=instructorReport['course code']*instructorReport['course code'] 

    #計算各個老師的一週的集中度（教師一週的授課堂數平方和）=> 取平均
    instructorReport = instructorReport.groupby('instructor').agg({"course code" : lambda x: np.sum(x)}).copy()
    instructorReport['course code']=instructorReport['course code']/(weekdays*dailyParts*dailyParts)*1000
    result1=1000-instructorReport['course code'].mean()
    #print("rule1: ",result1)
    return result1

#dailyConcentration(schedule, courseDetail)

# In[] #2 每段時間的課程離散度(取各Period課程數的平方和計算)
"""
Input: 課表schedule(list), 教室數量roomNum(int), 區塊數period(int), 課程總數totalCourseNum(int) 
Output: 課程離散度sdisp(number) 0~100分
"""
def sessionDispersion(schedule, roomNum, session, period, totalCourseNum):
    courseNum=0
    maxdiv=1000
    mindiv=0
    periodlist=[] #每個中period的課程數量

    #計算每個區塊中課程數量的平方和
    for i, x in enumerate(schedule):
        if x != '': #有課
            courseNum=courseNum+1
        if i%roomNum==roomNum-1: #每三個加總一次，存到list中，courseNum歸零
            periodlist.append(courseNum)
            courseNum=0
    squaresum=sum(i*i for i in periodlist) #平方和

    #計算平方和最大值&最小值
    if totalCourseNum<period:
        maxdiv=roomNum*roomNum*(totalCourseNum/roomNum)
        mindiv=1*1*totalCourseNum
    else: # totalCourseNum>period
        maxdiv=roomNum*roomNum*(session/roomNum)
        mindiv=totalCourseNum*totalCourseNum/period
        #這邊不考慮totalCourseNum>session的情況，因為這樣違背了條件限制[所有課都要被排入]

    #將平方和量化為0~1000分
    d=maxdiv-mindiv
    if d==0:
        sdisp=1000-(squaresum-mindiv)*1000
    else:
        sdisp=1000-(squaresum-mindiv)/d*1000
    return sdisp
    """
    #原本的
    #計算平方和最大值&最小值
    if totalCourseNum<period:
        fulfilledmax=totalCourseNum/roomNum
        mindiv=1
    elif totalCourseNum<=session:
        fulfilledmax=session/roomNum
        mindiv=totalCourseNum/period
    else:
        mindiv=totalCourseNum/period

    maxdiv=roomNum*roomNum*(fulfilledmax) 
    dividends=maxdiv-mindiv
    #print(dividends, maxdiv, mindiv, squaresum)
    sdisp=100-(squaresum-mindiv)/dividends*100 #量化為0~100分
    print(sdisp)
    """

# In[] #3 教室與人數有剛好match    
"""
Input: 一維度課表schedule(list), 計算索引的參數k(number)
Output: 人限差距分數cdiffscore(number) 0~1000分
"""
def capacityDifference(schedule, RoomDetail): 
    #生成45個session對應的教室
    RoomCapacityList = list(RoomDetail.cr_capacity)  #[60, 70, 80]
    RoomCapacityList = RoomCapacityList * ( weekdays * dailyParts) #[60, 70, 80, 60, 70, 80, 60, 70, 80, 60, 70, 80, 60, 70, 80, 60, 70, 80, 60, 70, 80, 60, 70, 80, 60, 70, 80, 60, 70, 80, 60, 70, 80, 60, 70, 80, 60, 70, 80, 60, 70, 80, 60, 70, 80]
    RoomCapacityList = pd.DataFrame({ 'RoomCapacity': RoomCapacityList})
    RoomCapacityList
    
    #schedule右邊新增一欄RoomCapacityList
    schedule_Detail_3 = pd.DataFrame({ 'course code': schedule})
    schedule_Detail_3 = pd.concat([schedule_Detail_3, RoomCapacityList], axis=1)
    
    #LEFT JOIN (schedule 與 CourseCapacityList)
    schedule_Detail_3['course code']=schedule_Detail_3['course code'].astype(str)
    courseDetail['course code']=courseDetail['course code'].astype(str)
    schedule_Detail_3 = pd.merge(schedule_Detail_3, courseDetail[['course code', 'Number of students']], how='left', on='course code')
    schedule_Detail_3.columns=['course code',   'rCapacity',  'cCapacity']
    schedule_Detail_3
    
    #計算rmax,rmin,cmax,cmin
    rmax = schedule_Detail_3.rCapacity.max()
    rmin = schedule_Detail_3.rCapacity.min()
    cmax = schedule_Detail_3.cCapacity.max()
    cmin = schedule_Detail_3.cCapacity.min()
    dividends=max(abs(rmax-cmin), abs(cmax-rmin), abs(cmax-rmax), abs(cmin-rmin))
    
    #計算每個course的分數
    cdiff=abs(schedule_Detail_3.rCapacity-schedule_Detail_3.cCapacity)
    if dividends==0:
        cdiffscore=1000-cdiff*1000
    else:    
        cdiffscore=1000-(cdiff/dividends*1000) #算出差距的百分比，距離越大分數越低
    result3=cdiffscore.mean()
    #print("rule3: ", result3)
    return result3

# In[] #4 課程數量：下午>早上>晚上
"""
Input: 一維度課表schedule(list), 計算索引的參數k(number)
Output: period數所佔比例
"""
def courseArrangement(schedule, k):
    periodSum=[]
    temp=0
    for i, x in enumerate(schedule):
        if x!='': #有課
            temp=temp+1
        if(i%k==k-1):
            periodSum.append(temp)
            temp=0
    weights=[0.3, 0.6, 0.1]
    result4=0
    for i, p in enumerate(periodSum):
        result4=result4+p*weights[i]
    psum=sum(periodSum)
    #加權period數除以全部period數，0~1000分越大越好
    if psum==0:
        result4=result4*1000
    else:  
        result4=(result4/psum*1000)
    #print("rule4: ", result4)
    return result4  

# In[] Objective Function
def ObjFun(schedule,courseDetail, roomNum, k, RoomDetail, session, period, totalCourseNum):
    weight=[0.4, 0.25, 0.25, 0.1]
    Objval=weight[0]*dailyConcentration(schedule, courseDetail, weekdays, dailyParts)+\
    weight[1]*sessionDispersion(schedule, roomNum, session, period, totalCourseNum)+\
    weight[2]*capacityDifference(schedule, RoomDetail)+\
    weight[3]*courseArrangement(schedule, k)
    #print(Objval)
    return Objval
#ObjFun(schedule,courseDetail, roomNum, k, RoomDetail, session, period, totalCourseNum)


# In[] 將一維list轉變成dataframe的課表
def ListToSchedule(schedule):
    """
        input: list 
        return: dataframe
    """
    schedule
    x = pd.DataFrame ( np.reshape(schedule, (3, 15)) )
    x = pd.concat([pd.DataFrame (['上午','下午','晚上']), x], axis=1)
    x.columns = [['','Mon','Mon','Mon','Tue','Tue','Tue','Wed','Wed','Wed','Thu','Thu','Thu','Fri','Fri','Fri'],['','Room1','Room2','Room3','Room1','Room2','Room3','Room1','Room2','Room3','Room1','Room2','Room3','Room1','Room2','Room3']]
    return(x)

#ListToSchedule(schedule_optimized)

# In[] feasible_test
    
import csv
dataset = []
course_name = []
classroom = []
professor_name = []

with open("data/course.csv","r",encoding="utf-8") as fIn:
    csvIn = csv.reader(fIn)
    for line in csvIn:
        dataset.append(line)
        course_name.append(line[0])
        classroom.append(line[2]) 
        professor_name.append(line[3]) 
        
course_name = course_name[1:]
classroom = classroom[1:]
professor_name = professor_name[1:]

def feasible_test(test_schedule):
    '''
    1.所有的課程應該都被排下去
    2.不可以有重複課程
    3.老師同一個時間不能出現在兩間教室(同一時段無重複教授)
    '''

    # 1.所有的課程應該都被排下去
    for data in course_name:
        if data == "":
            pass
        elif data in test_schedule: #課程皆可在原始資料中被找到
            pass
        else:
            # print("Error: 所有的課程應該都被排下去")
            return False

    # 2.不可以有重複課程
    for data in test_schedule:
        if data == "":
            pass
        elif test_schedule.count(data) == 1: #課程只有一個
            pass
        else:
            # print("Error: 不可以有重複課程")
            return False
        
    # 3.老師同一個時間不能出現在兩間教室(同一時段無重複教授)
    # (0 1 2),(3 4 5),(6 7 8)
    for i in range(0,45,3):
        if test_schedule[i] == "" or test_schedule[i+1] == "":
            pass
        else:
            course_name_index1 = course_name.index(test_schedule[i])
            course_name_index2 = course_name.index(test_schedule[i+1])
            if professor_name[course_name_index1] == professor_name[course_name_index2]:
                # print("發現衝突:({},{}), 位於時間({},{})".format(test_schedule[i],test_schedule[i+1],i,i+1))
                # print("Error: 老師同一個時間不能出現在兩間教室(同一時段無重複教授)")
                return False
        
        if test_schedule[i+1] == "" or test_schedule[i+2] == "":
            pass
        else:
            course_name_index2 = course_name.index(test_schedule[i+1])
            course_name_index3 = course_name.index(test_schedule[i+2])
            if professor_name[course_name_index2] == professor_name[course_name_index3]:
                # print("發現衝突:({},{}), 位於時間({},{})".format(test_schedule[i+1],test_schedule[i+2],i+1,i+2))
                # print("Error: 老師同一個時間不能出現在兩間教室(同一時段無重複教授)")
                return False
        
        if test_schedule[i] == "" or test_schedule[i+2] == "":
            pass
        else:
            course_name_index1 = course_name.index(test_schedule[i])
            course_name_index3 = course_name.index(test_schedule[i+2])
            if professor_name[course_name_index1] == professor_name[course_name_index3]:
                # print("發現衝突:({},{}), 位於時間({},{})".format(test_schedule[i],test_schedule[i+2],i,i+2))
                # print("Error: 老師同一個時間不能出現在兩間教室(同一時段無重複教授)")
                return False
 

#     # 4.教室不可重複使用
#     # (0 1 2),(3 4 5),(6 7 8)
#     for i in range(0,45,3):
#         if test_schedule[i] == "" or test_schedule[i+1] == "":
#             pass
#         else:
#             course_name_index1 = course_name.index(test_schedule[i])
#             course_name_index2 = course_name.index(test_schedule[i+1])
#             if classroom[course_name_index1] == classroom[course_name_index2]:
#                 print("發現衝突:({},{}), 位於時間({},{})".format(test_schedule[i],test_schedule[i+1],i,i+1))
#                 print("Error: 教室不可重複使用")
#                 return False
        
#         if test_schedule[i+1] == "" or test_schedule[i+2] == "":
#             pass
#         else:
#             course_name_index2 = course_name.index(test_schedule[i+1])
#             course_name_index3 = course_name.index(test_schedule[i+2])
#             if classroom[course_name_index2] == classroom[course_name_index3]:
#                 print("發現衝突:({},{}), 位於時間({},{})".format(test_schedule[i+1],test_schedule[i+2],i+1,i+2))
#                 print("Error: 教室不可重複使用")
#                 return False
        
#         if test_schedule[i] == "" or test_schedule[i+2] == "":
#             pass
#         else:
#             course_name_index1 = course_name.index(test_schedule[i])
#             course_name_index3 = course_name.index(test_schedule[i+2])
#             if classroom[course_name_index1] == classroom[course_name_index3]:
#                 print("發現衝突:({},{}), 位於時間({},{})".format(test_schedule[i],test_schedule[i+2],i,i+2))
#                 print("Error: 教室不可重複使用")
#                 return False

    return True
    
# In[] 生成initial solution (greedily) 
    
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

print("Random Initial Solution: ", generate(courseDetail, tNum, cNum, period))
#30['306008001', '307942001', '', '306525001', '356808001', '', '307851001', '306736001', '', '307867001', '307873001', '', '356019001', '356388001', '', '356387001', '356395001', '', '356813001', '306016022', '', '306000001', '307034001', '', '306737001', '356389001', '', '307857001', '306016002', '', '356425001', '307901001', '', '356461001', '307035001', '', '356822001', '307932001', '', '306016012', '356564001', '', '307870001', '306050011', '']
#33['306008001', '307870001', '307932001', '306525001', '307942001', '356564001', '307851001', '356808001', '306050011', '307867001', '306016022', '', '356019001', '307034001', '', '356387001', '356389001', '', '356813001', '356813002', '', '356813004', '306736001', '', '306000001', '307873001', '', '306737001', '356388001', '', '307857001', '356395001', '', '356425001', '306016002', '', '356461001', '307901001', '', '356822001', '356813003', '', '306016012', '307035001', '']

# In[] 生成initial solution (randomly) 
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
        if(feasible_test(blank_schedule)):
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
