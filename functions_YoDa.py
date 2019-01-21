#variables
roomNum=3 #教室數量
weekdays=5 #上課日子
dailyParts=3 #parts=將一天劃分為[早上、下午、晚上]
period=weekdays*dailyParts #15 一個weekdays中，不分教室的區塊總數
session=roomNum*weekdays*dailyParts #45 一個weekdays中，空教室的總數(一維陣列的長度)
k=weekdays*roomNum #15 [早上、下午、晚上] 一個part中的session數(索引調整參數)
# In[] 
# testing data
"""
schedule=['306000001','','306008001','','','306016002','356425001','','306016012','307873001','','307867001','307942001','','307870001',
 '306016022','307857001','306050011','356387001','356388001','307851001','306525001','','307035001','306736001','356395001','307034001','356461001','','306737001',
'307932001','','356822001','','356389001','356019001','356564001','','307901001','356813001','','356808001','','','']
"""

#initial schedule 預設為空直
schedule=[]
for i in range(session):
    schedule.append('')
# In[] 
#1 教授單日授課集中度(例如：老師一天從早上直接上課到晚上)


import pandas as pd
import numpy as np
#讀取courseDetail
courseDetail = pd.read_csv('data/course.csv')[['course code', 'Number of students', 'instructor']]
courseDetail['course code']=courseDetail['course code'].astype(str)
"""
Input: schedule(list), 含授課教師課程細節的courseDetail(dictionary)

Output: dailyConc(number) 0~100分 : (number of sessions - number of days + 1)/ number of sessions
"""
def dailyConcentration(schedule, courseDetail):
    #LEFT JOIN (schedule 與 courseDetail)
    schedule_Detail =  pd.DataFrame(schedule.copy(),  columns=['course code'])
    schedule_Detail['course code']=schedule_ValueInstructor['course code'].astype(str)
    schedule_Detail = pd.merge(schedule_Detail, courseDetail, how='left', on='course code')

    #生成45個session對應的Weekday
    WeekdayList=[]
    for i in range(session):
        print(i,':')
        if i%15 in [0,1,2]:
            WeekdayList.append(1)
        elif i%15 in [3,4,5]:
            WeekdayList.append(2)
        elif i%15 in [6,7,8]:
            WeekdayList.append(3)
        elif i%15 in [9,10,11]:
            WeekdayList.append(4)
        elif i%15 in [12,13,14]:
            WeekdayList.append(5)
    WeekdayList = pd.DataFrame({ 'weekday': WeekdayList})
    
    #schedule右邊新增一欄Weekday
    schedule_Detail = pd.concat([schedule_Detail, WeekdayList], axis=1)
    
    #計算各個老師的一週上課堂數、上課天數
    instructorReport = schedule_Detail.groupby('instructor').agg({"course code":'count', "weekday": pd.Series.nunique}).copy()
    instructorReport['instructor'] = instructorReport.index
    instructorReport.reset_index(level=0,drop=True, inplace=True)
    instructorReport.columns = ['NumberofSessions', 'NmberofDays', 'instructor']
    instructorReport
    
    #計算各個老師的分數：(number of sessions - number of days + 1)/ number of sessions
    instructorScore = (instructorReport.NumberofSessions - instructorReport.NmberofDays  + 1)/ instructorReport.NumberofSessions
    print(instructorScore)
    return instructorScore.mean()

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
def sessionDispersion(schedule, roomNum):
	courseNum=0
	periodlist=[] #每個中period的課程數量
	for i, x in enumerate(schedule):
	    if x!='' #有課
	        courseNum=courseNum+1
	    while i%roomNum==roomNum-1: #每三個加總一次，存到list中，courseNum歸零
	    	periodlist.append(courseNum)
	    	courseNum=0
	    	pass
	squaresum=sum(i*i for i in periodlist) #平方和
	###需改良為可變動的公式###
	maxdiv=roomNum*roomNum*10
	mindiv=(roomNum-1)*(roomNum-1)*15 
	dividends=maxdiv-mindiv
	###
	sdisp=(squaresum-mindiv)/dividends*100 #量化為0~100分
	sdisp
# In[] 
#3 教室與人數有剛好match    
"""
Input: 
教室人限rCapacity(number), 課程人限cCapacity(number)
教室人限最大值rmax(number), 最小值rmin(number)
課程人限最大值cmax(number), 最小值cmin(number)
Output: 人限差距分數cdiffscore(number) 0~100分
"""

def capacityDifference(rCapacity,cCapacity,rmax,rmin,cmax,cmin):
    dividends=max(rmax-cmin, cmax-cmin)
    cdiff=abs(rCapacity-cCapacity)   #差距 
    if cdiff==0:
    	cdiffscore=100
    else:
    	cdiffscore=100-(cdiff/dividends*100) #算出差距的百分比，距離越大分數越低
    return cdiffscore   

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
	print(periodSum)  #course number list [morning, afternoon, eveneing]
	return periodSum[1]/(sum(periodSum))  #下午period數除以全部period數，越大越好



# In[] 執行函數
#3
rCapacity=40
cCapacity=60
rmax=80
rmin=60
cmax=40
cmin=25
capacityDifference(rCapacity,cCapacity,rmax,rmin,cmax,cmin)#
#4
schedule=['306000001','','','','','','','','','','','','','','',
 '','307857001','','','','','','','','','356395001','','','','306737001',
'307932001','','356822001','','','','','','','','','','','','']
courseArrangement(schedule, k)

