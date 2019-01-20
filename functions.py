#variables
roomNum=3 #教室數量
weekdays=5 #上課日子
dailyParts=3 #parts=將一天劃分為[早上、下午、晚上]
period=weekdays*dailyParts #15 一個weekdays中，不分教室的區塊總數
session=roomNum*weekdays*dailyParts #45 一個weekdays中，空教室的總數(一維陣列的長度)
k=weekdays*roomNum #15 [早上、下午、晚上] 一個part中的session數(索引調整參數)

# testing data
"""
schedule=
['306000001','','306008001','','','306016002','356425001','','306016012','307873001','','307867001','307942001','','307870001',
 '306016022','307857001','306050011','356387001','356388001','307851001','306525001','','307035001','306736001','356395001','307034001','356461001','','306737001',
'307932001','','356822001','','356389001','356019001','356564001','','307901001','356813001','','356808001','','','']
"""

#initial schedule 預設為空直
schedule=[]
for i in range(45):
    schedule.append('')

#1 教授單日授課集中度(例如：老師一天從早上直接上課到晚上)
def dailyConcentration():

    print("concentration")


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
	        print(i,'TRUE')
	    else:    #沒課
	        print(i,'FALSE')
	    while i%3==2: #每三個加總一次，存到list中，courseNum歸零
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
    cdiffscore   


#4 課程數量：下午>早上>晚上
"""
Input: 一維度課表schedule(list), 計算索引的參數k(number)
Output: 各時段的課程數量加總periodSum(list) 
"""
def courseArrangement(schedule, k):
	periodSum=[]
	temp=0
	for i, x in enumerate(schedule):
	    if x!='' #有課
	        temp=temp+1
	        print(i,'TRUE')
	    else:    #沒課
	        print(i,'FALSE')
	    if(i%k==k-1):
	        periodSum.append(temp)
	periodSum #course number list [morning, afternoon, eveneing]



