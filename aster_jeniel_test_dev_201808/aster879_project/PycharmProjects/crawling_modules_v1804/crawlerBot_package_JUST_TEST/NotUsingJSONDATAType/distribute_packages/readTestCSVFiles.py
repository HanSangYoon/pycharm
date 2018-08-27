# CSV 파일 읽기 ======================================================================
import csv


def readCSV(searchTValue):

    #C:\python_project\aster879_project\PycharmProjects
    reader = csv.reader(
        open('C:\\python_project\\aster879_project\\PycharmProjects\\1_500Corp.csv', 'rt', encoding='utf-8-sig', newline=''), delimiter=' ', quotechar='|')

    print('함수안에서의 전달받은 값 : ', searchTValue)



    corpList = []
    for row in reader:
        corpList.append(', '.join(row))
    print('corpList : ', corpList)

    returnScore = 0
    #500대 기업 loop
    for row2 in corpList:
        #print()
        #print('row2 : ', row2) # 500대 기업 리스트 개별로 출력
        #print('len(searchTValue) :', len(searchTValue)) #예: 4

        returnScore1 = 0

        for loopInt in range(len(searchTValue)):
            #print('searchTValue['+str(loopInt)+'] :', searchTValue[loopInt])
            if searchTValue[loopInt] in row2:
                print('searchTValue[' + str(loopInt) + '] :', searchTValue[loopInt])
                returnScore1 += 10
                break

        #print('Score1 :', returnScore1)
        returnScore += returnScore1

    print(returnScore)
    return returnScore


returnedResultDict = {'Name': 'Zara', 'Age': 27, '성별': 'man', '직장이력':['삼성', '금성', '엘지', '럭키', '텐스페이스']}
search_t_value = returnedResultDict.get('직장이력', [])
#search_t_valueText = '__'.join(search_t_value)

print('직장이력:', search_t_value)

returnValue = readCSV(search_t_value)





print('return:', returnValue)