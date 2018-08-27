from pymongo import MongoClient


class MongoDB_CRUD:

    def mngDB_connection(hereWork):
        Client = MongoClient('localhost', 27017)
        db_instagramCrawledData = Client[hereWork + 'CrawledData']
        collectionDatabase_SNS = db_instagramCrawledData['PostText_' + hereWork]

        return collectionDatabase_SNS

    def mngDB_INSERT(hereWork, userSNS_URL, userSNS_dictionaryTypeData, currDate, collectionName_SNS):
        try:
            collectionName_SNS.insert({'Description(user_'+hereWork+'_URL)':userSNS_URL, hereWork + '_data':userSNS_dictionaryTypeData, 'inserted date':currDate})
            print('DB에 데이터를 정상적으로 INSERT 하였습니다.')
        except Exception as e:
            print('데이터 INSERT를 실패하였습니다.', e)