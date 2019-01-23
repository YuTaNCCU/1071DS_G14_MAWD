import csv
dataset = []
course_name = []
classroom = []
professor_name = []

with open("course.csv","r",encoding="utf-8") as fIn:
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
            print("Error: 所有的課程應該都被排下去")
            return False

    # 2.不可以有重複課程
    for data in test_schedule:
        if data == "":
            pass
        elif test_schedule.count(data) == 1: #課程只有一個
            pass
        else:
            print("Error: 不可以有重複課程")
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
                print("發現衝突:({},{}), 位於時間({},{})".format(test_schedule[i],test_schedule[i+1],i,i+1))
                print("Error: 老師同一個時間不能出現在兩間教室(同一時段無重複教授)")
                return False
        
        if test_schedule[i+1] == "" or test_schedule[i+2] == "":
            pass
        else:
            course_name_index2 = course_name.index(test_schedule[i+1])
            course_name_index3 = course_name.index(test_schedule[i+2])
            if professor_name[course_name_index2] == professor_name[course_name_index3]:
                print("發現衝突:({},{}), 位於時間({},{})".format(test_schedule[i+1],test_schedule[i+2],i+1,i+2))
                print("Error: 老師同一個時間不能出現在兩間教室(同一時段無重複教授)")
                return False
        
        if test_schedule[i] == "" or test_schedule[i+2] == "":
            pass
        else:
            course_name_index1 = course_name.index(test_schedule[i])
            course_name_index3 = course_name.index(test_schedule[i+2])
            if professor_name[course_name_index1] == professor_name[course_name_index3]:
                print("發現衝突:({},{}), 位於時間({},{})".format(test_schedule[i],test_schedule[i+2],i,i+2))
                print("Error: 老師同一個時間不能出現在兩間教室(同一時段無重複教授)")
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


