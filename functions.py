#variables
weekdays=5
roomNum=3
dailyPeriod=3 #morning, afternoon, evening
sessions=weekdays*roomNum*dailyPeriod #45
k=weekdays*roomNum #15
# testing data
"""
schedule=
['',
 1,
 2,
 3,
 4,
 5,
 6,
 '',
 '',
 '',
 '',
 '',
 12,
 13,
 14,
 '',
 16,
 17,
 18,
 19,
 '',
 21,
 22,
 '',
 24,
 25,
 26,
 27,
 28,
 '',
 30,
 31,
 32,
 33,
 34,
 '',
 36,
 37,
 38,
 '',
 40,
 41,
 42,
 43,
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
def capacityDifference(rCapacity,cCapacity):
    d=rCapacity-cCapacity
    print("d")    #要想一個更好的量化方式嗎？還是就以差值為主？
    
#4 課程數量：下午>早上>晚上
def courseArrangement():
	k=15
	periodSum=[]
	temp=0
	for i, x in enumerate(schedule):
	    if x!=i: #有課
	        temp=temp+1
	        print(i,'TRUE')
	    else:    #沒課
	        print(i,'FALSE')
	    if(i%k==k-1):
	        periodSum.append(temp)
	periodSum #course number list [morning, afternoon, eveneing]



