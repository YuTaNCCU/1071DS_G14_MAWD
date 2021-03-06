# In[] 
import pandas as pd
import numpy as np
#讀取courseDetail
courseDetail = pd.read_csv('data/course.csv')[['course code', 'Number of students', 'instructor']]
courseDetail['course code']=courseDetail['course code'].astype(str)
RoomDetail = pd.read_csv('data/classroom.csv')[['classroom', 'cr_capacity']]

#variables
roomNum=3 #教室數量
weekdays=5 #上課日子
dailyParts=3 #parts=將一天劃分為[早上、下午、晚上]
period=weekdays*dailyParts #15 一個weekdays中，不分教室的區塊總數
session=roomNum*weekdays*dailyParts #45 一個weekdays中，空教室的總數(一維陣列的長度)
k=weekdays*roomNum #15 [早上、下午、晚上] 一個part中的session數(索引調整參數)
totalCourseNum=30

#initial schedule 預設為空直
schedule=[]
for i in range(session):
    schedule.append('')
    
# testing data
"""
schedule=['306000001','','306008001','','','306016002','356425001','','306016012','307873001','','307867001','307942001','','307870001',
 '306016022','307857001','306050011','356387001','356388001','307851001','306525001','','307035001','306736001','356395001','307034001','356461001','','306737001',
'307932001','','356822001','','356389001','356019001','356564001','','307901001','356813001','','356808001','','','']
"""

# In[] 
#1 教授單日授課集中度(例如：老師一天從早上直接上課到晚上)
"""
Input: schedule(list), 含授課教師課程細節的courseDetail(dictionary)

Output: dailyConc(number) 0~100分 : (number of sessions - number of days + 1)/ number of sessions
"""
def dailyConcentration(schedule, courseDetail):
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
    
    #計算各個老師的一週各天的集中度（一天的授課堂數/dailyParts）> 再各天平均
    instructorReport = instructorReport.groupby('instructor').agg({"course code" : lambda x: np.mean(x/dailyParts)}).copy()
    
    #回傳每一位老師平均集中度的平均值 > 再 （100-集中度）
    return (100 - instructorReport['course code'].mean()*100)

schedule=['306000001','','','356461001','','','','','','','','','','','',
 '','307857001','','','','','','','','','356395001','','','','306737001',
'307932001','','356822001','','','','','','','','','','','','']
dailyConcentration(schedule, courseDetail)


# In[] 
#2 每段時間的課程離散度(取各Period課程數的平方和計算)
"""
一個時段三堂課、一個時段兩堂課、一個時段一堂課
以30堂課來排
最小15個時段都兩門=15*2^2=60
最大10個時段有3門=10*3^2=90
Input: 課表schedule(list), 教室數量roomNum(number)
Output: 課程離散度sdisp(number) 0~100分
"""
def sessionDispersion(schedule, roomNum, session, period, totalCourseNum):
    courseNum=0
    fulfilledmax=session/roomNum
    periodlist=[] #每個中period的課程數量
    for i, x in enumerate(schedule):
        if x != '': #有課
            courseNum=courseNum+1
        if i%roomNum==roomNum-1: #每三個加總一次，存到list中，courseNum歸零
            periodlist.append(courseNum)
            courseNum=0
    squaresum=sum(i*i for i in periodlist) #平方和
    
    if totalCourseNum<period:
        fulfilledmax=totalCourseNum/roomNum
        mindiv=1
    elif totalCourseNum>=session:
        fulfilledmax=session/roomNum
        mindiv=totalCourseNum/period
    else:
        mindiv=totalCourseNum/period

    maxdiv=roomNum*roomNum*(fulfilledmax) 
    dividends=maxdiv-mindiv
    #print(dividends, maxdiv, mindiv, squaresum)
    sdisp=(squaresum-mindiv)/dividends*100 #量化為0~100分

    return sdisp



# In[] 
#3 教室與人數有剛好match    
"""
Input: 
一維度課表schedule(list), 計算索引的參數k(number)
Output: 人限差距分數cdiffscore(number) 0~100分
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
    dividends=max(abs(rmax-cmin), abs(cmax-rmin))
    
    #計算每個course 的分數
    cdiff=abs(schedule_Detail_3.rCapacity-schedule_Detail_3.cCapacity)   #差距 
    cdiffscore=100-(cdiff/dividends*100) #算出差距的百分比，距離越大分數越低
    
    return cdiffscore.mean()
capacityDifference(schedule, RoomDetail)
# In[] 
#4 課程數量：下午>早上>晚上
"""
Input: 一維度課表schedule(list), 計算索引的參數k(number)
Output: 下午period數所佔比例
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
	periodSum  #course number list [morning, afternoon, eveneing]
	weights=[0.3, 0.5, 0.2]
	result=0
	for i, p in enumerate(periodSum):
	    result=result+p*weights[i]
	return (result/sum(periodSum)*100)  #加權period數除以全部period數，0~100分越大越好

schedule=['306000001','','','','','','','','','','','','','','',
 '','307857001','','','','','','','','','356395001','','','','306737001',
'307932001','','356822001','','','','','','','','','','','','']

# In[]
# Objective Function

#暫時剔除#2
def ObjFun(schedule,courseDetail, roomNum, k, RoomDetail):
    weight=[50, 25, 15, 5]
    value=weight[0]*dailyConcentration(schedule, courseDetail)+weight[2]*capacityDifference(schedule, RoomDetail)+weight[3]*courseArrangement(schedule, k)
    return value
ObjFun(schedule,courseDetail, roomNum, k, RoomDetail)


def ObjFun(schedule,courseDetail, roomNum, k, RoomDetail, session, period, totalCourseNum):
    weight=[50, 25, 15, 5]
    Objval=weight[0]*dailyConcentration(schedule, courseDetail)+\
    weight[1]*sessionDispersion(schedule, roomNum, session, period, totalCourseNum)+\
    weight[2]*capacityDifference(schedule, RoomDetail)+\
    weight[3]*courseArrangement(schedule, k)
    return Objval

ObjFun(schedule,courseDetail, roomNum, k, RoomDetail, session, period, totalCourseNum)













