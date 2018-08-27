# CSV 파일 읽기 ======================================================================
import csv


def readCSV(listValue):
    resultList = []

    with open('C:\python_project\\aster879_project\\PycharmProjects\\1_500Corp.csv', 'rt',
              encoding='utf-8') as csvCorpNameFile:
        reader = csv.reader(csvCorpNameFile, delimiter=',')
        print('@#$@#$', list(reader))

        for row in reader:
            if row[1].strip() == listValue:
                resultList.append(listValue)
            else:
                print('일치하는 항목이 없습니다.')

        print('csv file result : ', resultList)


readCSV('삼성')