# CSV 파일 읽기 ======================================================================
import csv


def readCSV():
    resultList = []

    with open('C:\\dev_syhan\\aster_jeniel_test_dev_201808\\긍정어4.csv', 'rt', encoding='utf-8-sig') as csvCorpNameFile:
        reader = csv.reader(csvCorpNameFile, delimiter=',')
        print('@#$@#$', list(reader))

        for row in reader:
            print(row)
            resultList.append(row)


        print('csv file read : ', resultList)


readCSV()