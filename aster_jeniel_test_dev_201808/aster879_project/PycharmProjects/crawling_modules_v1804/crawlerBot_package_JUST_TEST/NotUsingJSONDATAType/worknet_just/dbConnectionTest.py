import pymysql

class DatabaseConnection_origin:
    def __init__(self):
        print()

    def conn(self):
        try:
            #localhost
            self.connection = pymysql.connect(host='uml.kr', port=3366,
                       user='just_aster_dba', password='!just716811',
                       db='just', charset='utf8')

            self.connection.autocommit = True
            self.cursor = self.connection.cursor()


            print('DB connection completed')

        except:
            print('Cannot connect to Database')

    def select_record(self):
        try:
            selectedDataList = []
            self.cursor.execute("SELECT no_index, articleUniqueNum FROM just_crawled_worknet ORDER BY no_index ASC;")
            cats = self.cursor.fetchall()
            for cat in cats:
                print('cat : ', cat)

                # articleUniqueNum 만 list 에 넣기 위함
                selectedDataList.append(cat[1])
                # print("each rows : {}".format(cat))

            self.connection.close()

            return selectedDataList

        except Exception as e:
            print('select_record -> ', e)
            return None


    def insert_new_record(self, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10,
                          f11, f12, f13, f14, f15, f16, f17, f18, f19, f20,
                          f21, f22, f23, f24, f25, f26, f27, f28, f29, f30,
                          f31, f32, f33, f34, f35, f36, f37, f38, f39, f40,
                          f41, f42, f43, f44, f45, f46, f47, f48, f49, f50,
                          f51, f52, f53, f54, f55, f56):

        dbInsertResult = False

        try:
            insert_command = "INSERT INTO just_crawled_worknet(articleUniqueNum, corpNm," \
                             " corpWantJob, corpRecruitArticleTitle, searchArticleCnt, applicantArticleCnt," \
                             " corpImgDir, corpNm_detl, ceoNm, workerCnt, jabon, yearIncome, jobKind, jobKind_main," \
                             " corpAddr, homepage, recruitJobKind, jobKindKeyword, relatedJobKind, whatWork, experOpt, " \
                             " eduCond, workArea, wageCond, hireType_detl, hireCnt, workPlace, industCommnt," \
                             " nearSubway, wageCond_detl, mealOffer, workTime, jobType, socialEnsure, retirePay, applyDueDate, howToRecruit_detl, howToApply_detl," \
                             " applyDoc, applyDocAttach, bilingual, collgMajor, license, comCap, prfrFactor_detl, wishHireMil, wishHireDisabled," \
                             " etcPrefer, welfare, facltDisabled, moreHireCond, recruitMngr, recruitMngrTel1, recruitMngrTel2, faxNo, recruitMngrEmail) " \
                             "VALUES ('" + f1 + "','" + f2 + "','" + f3 + "','" + f4 + "','" + f5 + "','" + \
                             f6 + "','" + f7 + "','" + f8 + "','" + f9 + "','" + f10 + "','" + \
                             f11 + "','" + f12 + "','" + f13 + "','" + f14 + "','" + f15 + "','" + \
                             f16 + "','" + f17 + "','" + f18 + "','" + f19 + "','" + f20 + "','" + \
                             f21 + "','" + f22 + "','" + f23 + "','" + f24 + "','" + f25 + "','" + \
                             f26 + "','" + f27 + "','" + f28 + "','" + f29 + "','" + f30 + "','" + \
                             f31 + "','" + f32 + "','" + f33 + "','" + f34 + "','" + f35 + "','" + \
                             f36 + "','" + f37 + "','" + f38 + "','" + f39 + "','" + f40 + "','" + \
                             f41 + "','" + f42 + "','" + f43 + "','" + f44 + "','" + f45 + "','" + \
                             f46 + "','" + f47 + "','" + f48 + "','" + f49 + "','" + f50 + "','" + \
                             f51 + "','" + f52 + "','" + f53 + "','" + f54 + "','" + f55 + "','" + \
                             f56 + "')"

            print(insert_command)
            self.cursor.execute(insert_command)

            self.connection.commit()
            self.connection.close()

            dbInsertResult = True

            return dbInsertResult

        except Exception as e:
            print('DBINSERT_FALSE', e)

            return dbInsertResult