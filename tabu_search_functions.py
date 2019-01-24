#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 23:38:50 2019

@author: yuta_mac
"""
   
def TabuSearch():
    ### Loading Package & Data
    
    import pandas as pd
    import numpy as np
    import functions
    import feasible_test as ft
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
    totalCourseNum=len(courseDetail['course code'])
    
    # testing data
    temp_schedule_simple=['306000001','','','','','','','','','','','','','','',
     '','307857001','','','','','','','','','356395001','','','','306737001',
    '307932001','','356822001','','','','','','','','','','','','']
    temp_schedule_feasible=['306000001','','306008001','','','306016002','356425001','','306016012','307873001','','307867001','307942001','','307870001',
     '306016022','307857001','306050011','356387001','356388001','307851001','306525001','','307035001','306736001','356395001','307034001','356461001','','306737001',
    '307932001','','356822001','','356389001','356019001','356564001','','307901001','356813001','','356808001','','','']
    
    
    
    ### Initial Solution 愛麗絲方法
    import test 
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
    
    InitialSolution = test.generate(courseDetail, tNum, cNum, period)
    
    ### Initial Solution 嗡嗡方法
    import new_random_initial_solution as new_init_sol
    InitialSolution = new_init_sol.get_schedule()
    
    ### Tabu Search
    
    ########################################################################
    #參考來源： https://github.com/100/Solid/edit/master/Solid/TabuSearch.py＃
    ########################################################################
    
    from random import choice, randint, random
    from string import ascii_lowercase
    from copy import deepcopy
    from abc import ABCMeta, abstractmethod
    from copy import deepcopy
    from collections import deque
    from numpy import argmax
    
    class TabuSearch:
        """
        Conducts tabu search
        """
        __metaclass__ = ABCMeta
    
        cur_steps = None
    
        tabu_size = None
        tabu_list = None
    
        initial_state = None
        current = None
        best = None
    
        max_steps = None
        max_score = None
    
        def __init__(self, initial_state, tabu_size, max_steps, max_score=None):
            """
    
            :param initial_state: initial state, should implement __eq__ or __cmp__
            :param tabu_size: number of states to keep in tabu list
            :param max_steps: maximum number of steps to run algorithm for
            :param max_score: score to stop algorithm once reached
            """
            self.initial_state = initial_state
    
            if isinstance(tabu_size, int) and tabu_size > 0:
                self.tabu_size = tabu_size
            else:
                raise TypeError('Tabu size must be a positive integer')
    
            if isinstance(max_steps, int) and max_steps > 0:
                self.max_steps = max_steps
            else:
                raise TypeError('Maximum steps must be a positive integer')
    
            if max_score is not None:
                if isinstance(max_score, (int, float)):
                    self.max_score = float(max_score)
                else:
                    raise TypeError('Maximum score must be a numeric type')
    
        def __str__(self):
            return ('TABU SEARCH: \n' +
                    'CURRENT STEPS: %d \n' +
                    'BEST SCORE: %f \n' +
                    'BEST MEMBER: %s \n\n') % \
                   (self.cur_steps, self._score(self.best), str(self.best))
    
        def __repr__(self):
            return self.__str__()
    
        def _clear(self):
            """
            Resets the variables that are altered on a per-run basis of the algorithm
    
            :return: None
            """
            self.cur_steps = 0
            
            #deque(maxlen=N) 创建了一个固定长度的队列，当有新的记录加入而队列已满时会自动移动除最老的那条记录
            self.tabu_list = deque(maxlen=self.tabu_size) 
            self.current = self.initial_state
            self.best = self.initial_state
    
        @abstractmethod
        def _score(self, state):
            """
            Returns objective function value of a state
    
            :param state: a state
            :return: objective function value of state
            """
            pass
    
        @abstractmethod
        def _neighborhood(self):
            """
            Returns list of all members of neighborhood of 
            state, given self.current
    
            :return: list of members of neighborhood
            """
            pass
    
        def _best(self, neighborhood):
            """
            Finds the best member of a neighborhood
    
            :param neighborhood: a neighborhood
            :return: best member of neighborhood
            """
            return neighborhood[argmax([self._score(x) for x in neighborhood])]
    
        def run(self, verbose=True):
            """
            Conducts tabu search
    
            :param verbose: indicates whether or not to print progress regularly
            :return: best state and objective function value of best state
            """
            self._clear()
            for i in range(self.max_steps):
                self.cur_steps += 1
    
                if ((i + 1) % 50 == 0) and verbose:
                    print(self)
    
                neighborhood = self._neighborhood()
                neighborhood_best = self._best(neighborhood)
    
                while True:
                    if all([x in self.tabu_list for x in neighborhood]):
                        print("TERMINATING - NO SUITABLE NEIGHBORS")
                        return self.best, self._score(self.best)
                    if neighborhood_best in self.tabu_list: 
                        #使用 Aspiration 
                        if self._score(neighborhood_best) > self._score(self.best):
                            self.tabu_list.append(neighborhood_best)
                            self.best = deepcopy(neighborhood_best)
                            break
                        else:
                            neighborhood.remove(neighborhood_best)
                            neighborhood_best = self._best(neighborhood)
                    else:
                        self.tabu_list.append(neighborhood_best)
                        self.current = neighborhood_best
                        if self._score(self.current) > self._score(self.best):
                            self.best = deepcopy(self.current)
                        break
    
                if self.max_score is not None and self._score(self.best) > self.max_score:
                    print("TERMINATING - REACHED MAXIMUM SCORE")
                    return self.best, self._score(self.best)
            print("TERMINATING - REACHED MAXIMUM STEPS")
            return self.best, self._score(self.best)
    
    
    ### 繼承與設定參數
    class TabuSearchCustomized(TabuSearch):
        """
        Tries to get  
        """
        def _neighborhood(self):
            member = list(self.current)
            neighborhood = []
            for _ in range(50): #鄰居數
                neighbor = deepcopy(member)
                #SWAP:
                for _ in range(5): # SWAP次數
                    NeighborList = list(range(session)) #[1,2,...44,45]
                    session1 = choice(NeighborList) #抽第一個位置
                    NeighborList.remove(session1)  #抽過的位置從list中移除
                    #NeighborList.remove((session1//roomNum)*roomNum+0)
                    #NeighborList.remove((session1//roomNum)*roomNum+1)
                    #NeighborList.remove((session1//roomNum)*roomNum+2)
                    session2 = choice(NeighborList)  #抽第二個位置
                    SwapTemp = neighbor[session1]  #二值交換
                    neighbor[session1]  = neighbor[session2] #二值交換
                    neighbor[session2]  = SwapTemp  #二值交換  
                if ft.feasible_test( neighbor ) :  #檢查這個鄰居是否feasible
                    neighborhood.append(neighbor) #feasible的鄰居放入備選list（neighborhood）
            return neighborhood
    
        def _score(self, state):
            return functions.ObjFun(state,courseDetail, roomNum, k, RoomDetail, session, period, totalCourseNum) #填入obj. fum.
    
    
    print('Initial Solution: \n',temp_schedule_feasible)
    print('Initial Obj. Val.: ',functions.ObjFun(InitialSolution,courseDetail, roomNum, k, RoomDetail, session, period, totalCourseNum) )
    
    
    #ScoreRecord=[]
   # Schedule_optimized=[]
   # TimeRecord=[]
    
    import time
    #for i in range(1):
    start_time = time.time()
    TSRun = TabuSearchCustomized(InitialSolution, 10, 100, max_score=None) #填入initial solution： Tabu List數, 迭代次數
    TSRun = TSRun.run()
    #print(TSRun)
    #ScoreRecord.append(TSRun[1])
    #Schedule_optimized.append(TSRun[0])
    #TimeRecord.append(time.time() - start_time)

    
    return TSRun[1], TSRun[0], (time.time() - start_time)

#a = TabuSearch()
