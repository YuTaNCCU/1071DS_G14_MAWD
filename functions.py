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
"""
Input: schedule(list), 含授課教師課程細節的courseDetail(dictionary)

Output: dailyConc(number) 0~100分
"""
def dailyConcentration(schedule, courseDetail):
	tschedule=[] #儲存老師名字的課表
	tname={} #儲存有授課的老師名字列表(不重複set)

	for x in schedule:
		if x!='':	#有課
			tschedule.append(courseDetail[x])
			tname.add(courseDetail[x])
		else:		#沒課
			tschedule.append('')
	#########################卡住了...需思考如何使用k設計條件單日授課量###########################
	for y in tname: #在課表中搜尋所有老師的名字
		for z in schedule:
			if courseDetail[z]==y: #這堂課是這個老師授課的
				courseNum=courseNum+1
		    while "條件": #每三個加總一次，存到list中，courseNum歸零
		    	periodlist.append(courseNum)
		    	courseNum=0
		    	pass
    dailyConc

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
	periodSum  #course number list [morning, afternoon, eveneing]
	weights=[0.3, 0.5, 0.2]
	result=0
	for i, p in enumerate(periodSum):
	    result=result+p*weights[i]
	return (result/sum(periodSum)*100)  #加權period數除以全部period數，0~100分越大越好

schedule=['306000001','','','','','','','','','','','','','','',
 '','307857001','','','','','','','','','356395001','','','','306737001',
'307932001','','356822001','','','','','','','','','','','','']

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
courseArrangement(schedule, k)

