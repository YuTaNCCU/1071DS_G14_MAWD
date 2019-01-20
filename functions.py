#variables
weekdays=5
roomNum=3
dailyPeriod=3 #morning, afternoon, evening
sessions=weekdays*roomNum*dailyPeriod #45
k=weekdays*roomNum #15
# testing data
"""
schedule=
['306000001',
 '',
 '306008001',
 '',
 '',
 '306016002',
 '356425001',
 '',
 '306016012',
 '307873001',
 '',
 '307867001',
 '307942001',
 '',
 '307870001',
 '306016022',
 '307857001',
 '306050011',	
 '356387001',	
 '356388001',	
 '307851001',	
 '306525001',
 '',
 '307035001',	
 '306736001',	
 '356395001',	
 '307034001',	
 '356461001',
 '',
 '306737001',
'307932001',
'',
 '356822001',
 '',
'356389001',	
'356019001',	
'356564001',
'',
'307901001',	
'356813001',
'',
'356808001',
'',
'',
'']
"""

#initial schedule
schedule=[]
for i in range(45):
    schedule.append(i)

#1 教授單日授課集中度(例如：老師一天從早上直接上課到晚上)
def dailyConcentration():

    print("concentration")

#2 每段時間的課程離散度(一個時段三堂課、一個時段兩堂課)
def sessionDispersion():
    print("dispersion")

#3 教室與人數有剛好match    
"""
Input: 
教室人限rCapacity(number), 課程人限cCapacity(number)
教室人限最大值rmax(number), 最小值rmin(number)
課程人限最大值cmax(number), 最小值cmin(number)
Output: 人限差距分數dscore(number) 0~100分
"""
def capacityDifference(rCapacity,cCapacity,rmax,rmin,cmax,cmin):
    dividends=max(rmax-cmin, cmax-cmin)
    d=abs(rCapacity-cCapacity)    
    if d==0:
    	dscore=100
    else:
    	dscore=100-(d/dividends*100) #距離越大分數越低
    dscore   

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



