# 1071DS_G14_MAWD

決策科學 final
===
Google Doc 共編
https://docs.google.com/document/d/18crK7lUqpjKy1OtneuQHkQyf6lldcqRK5JMGlJIwJc0/edit?fbclid=IwAR05wxzy7KdWIRah29iPHdlDQAeoBxvySg0IDsFB0rpDbo4vfNTpEdnXwgs
===
程式碼共編
https://colab.research.google.com/drive/1__JM4b3cDpwIyptyBWbpMLkKv9UO2kIu?fbclid=IwAR3TDHKTH2o-H3kcKI8-kDz2xa9M3JNnRgSwpcp3rG810q5pmFYW_Uzja7s#scrollTo=515qI2zaWd3c

## 個人報告
[嗡嗡](https://docs.google.com/presentation/d/1cyp33TGLdpBwX97b1FlG2vVIQQW1ZDWvFxHvzJoYBZI/edit?fbclid=IwAR2PdDUBbrLZk_yNjWUVX58OlgYLSj-mbWM0ARinMhdn0zgHsX1Z8fA_sL8#slide=id.p)
[Alice](https://drive.google.com/file/d/1hAR_c18il9SYq_RdQNqLzUTTR0aJlBem/view?usp=sharing)
[達達](
https://docs.google.com/presentation/d/1pKz6ZSkA0tLFegXxvCbhtDDNksZ3vhXRdw-1fvUxSwY/edit
)
GITHUB：https://github.com/YuTaNCCU/1071DS_G14_MAWD/graphs/contributors?fbclid=IwAR07l0jA4C_xjEsKeBPmiRjg7oc0quzjxoMlqd2G2tZJRCU8SCf8wB4gcvk

## 決策變數
* 課程
* 教室
* 時間

## 考慮的演算法
先選一個，或是全部逐個比較
* GA
* TABU
* ANN
* 蝙蝠
* 鯨魚



## 課程資訊(input需要的測試資料)
* 課名(課程代號)
* 授課老師
* (學生人數)
* (老師有空的時間)

課程時段呈現如下 

| 一 | 二 | 三 | 四 | 五 |
| -------- | -------- | -------- | -------- | -------- | -------- |
| * | * | * | * | * |
| 中午 | 中午 | 中午 | 中午 | 中午 |
| * | * | * | * | * |
|晚間|晚間|晚間|晚間|晚間|
| * | * | * | * | * |


## 簡化版本的題目
* 一週五天
* 一天三時段
* 一個時段有三間教室
:::success
一共45個時段可以被排課
:::

## 限制條件(括弧內為軟限制條件，不符合也能是個能用結果)
1. 所有的課程應該都被排下去
2. 老師同一個時間不能出現在兩間教室
3. 教室不可重複使用
:::danger
* 至少限制條件random的結果應該要feasible(可以用但不好的解）
:::


## 目標條件(optimal的定義，決定feasible中哪些是比較好的答案)
:::warning
nonfeasible(不能用的解) ->
 feasible(是解，但不夠好) ->
 optimal(最佳解)
:::

* 越符合真實情況的條件，分數越高(軟限制條件，不符合也能是個能用結果)

可以最後給個加權，算合適分數高低(怎麼樣算夠optimal的解)
1. 教授單日授課集中度(例如：老師一天從早上直接上課到晚上)
2. 每段時間的課程離散度(一個時段三堂課、一個時段兩堂課)
3. 教室與人數有剛好match
> * 超過人數數量
> * (Yes/No)符不符合：教室人數 < 修課人數
> * (教室資源浪費問題，教室人數 >> 修課人數)
4. 課程數量：下午>早上>晚上




## 處理流程(我們的algorithm)
* random解階段
> 1. 將 nonfeasible 的解直接處理掉，只留下feasible的解
> (nonfeasible 的解：不符合嚴格限制條件的解)

* 計算分數 (代表optimal的程度)階段
> 1. 只有 feasible 的解 才能算分數
> 1. 計算目標條件符合程度，並計算加權分數
> 1. 得到該課表的得分(optimal的程度

---


## 小麥的代辦事項
生假資料：
* 教室
    * 人數限制
* 課程：
    課程總數不要超過30，不然計算的課程離散度會難以產生差別。
    * 課程名稱(ID)
    * 授課教師：最多不要超過10個教師，每個老師授課數為2-6堂，不然顯示不出限制二的重要性
    * 修課人限：用來計算目標函數3的契合度
* 教師沒空的時間(X)

## Alice的代辦事項
1. 寫一個objective function計算分數
* 用numpy array存
* 用pandas dataframe
* 直接用一維的list，二維也可以(V)
2. initial random solution

## 嗡嗡 
查詢開源的程式碼:GA

https://github.com/100/Solid/blob/master/Solid/EvolutionaryAlgorithm.py

## 游達
查詢開源的程式碼:TS

https://github.com/100/Solid
https://github.com/100/Solid/blob/master/Solid/TabuSearch.py

https://blog.csdn.net/adkjb/article/details/81712969
