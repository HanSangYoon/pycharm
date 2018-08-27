
#!/usr/bin/python
import pymysql

'''
Python에서 MySQL에 있는 데이타를 사용하는 일반적인 절차는 다음과 같다.

1. PyMySql 모듈을 import 한다
2. pymysql.connect() 메소드를 사용하여 MySQL에 Connect 한다. 호스트명, 로그인, 암호, 접속할 DB 등을 파라미터로 지정한다.
3. DB 접속이 성공하면, Connection 객체로부터 cursor() 메서드를 호출하여 Cursor 객체를 가져온다. DB 커서는 Fetch 동작을 관리하는데 사용되는데, 만약 DB 자체가 커서를 지원하지 않으면, Python DB API에서 이 커서 동작을 Emulation 하게 된다.
4. Cursor 객체의 execute() 메서드를 사용하여 SQL 문장을 DB 서버에 보낸다.
5. SQL 쿼리의 경우 Cursor 객체의 fetchall(), fetchone(), fetchmany() 등의 메서드를 사용하여 데이타를 서버로부터 가져온 후, Fetch 된 데이타를 사용한다.
6. 삽입, 갱신, 삭제 등의 DML(Data Manipulation Language) 문장을 실행하는 경우, INSERT/UPDATE/DELETE 후 Connection 객체의 commit() 메서드를 사용하여 데이타를 확정 갱신한다.
7. Connection 객체의 close() 메서드를 사용하여 DB 연결을 닫는다.
'''

class DatabaseConnection_jeniel:
    def __init__(self):

        try:
            self.connection = pymysql.connect(host='uml.kr', port=3366,
                       user='just_aster_dba', password='!just716811',
                       db='just', charset='utf8')

            self.connection.autocommit = True
            self.cursor = self.connection.cursor()

            print('DB connection completed')

        except:
            print('Cannot connect to Database')

    def create_table(self):
        create_table_query = "CREATE TABLE `facebook_crawled_just` (\
                                `no_index` INT(11) NOT NULL AUTO_INCREMENT,\
                                `insertedTime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,\
                                `userName` VARCHAR(50) NULL DEFAULT NULL,\
                                `birthday` VARCHAR(50) NULL DEFAULT NULL,\
                                `birthday_luna` VARCHAR(50) NULL DEFAULT NULL,\
                                `sex` VARCHAR(50) NULL DEFAULT NULL,\
                                `bloodType` VARCHAR(50) NULL DEFAULT NULL,\
                                `addr` VARCHAR(100) NULL DEFAULT NULL,\
                                `facebookUrl` VARCHAR(50) NULL DEFAULT NULL,\
                                `website` VARCHAR(50) NULL DEFAULT NULL,\
                                `snsLink` VARCHAR(50) NULL DEFAULT NULL,\
                                `religion` VARCHAR(50) NULL DEFAULT NULL,\
                                `cellPhone` VARCHAR(50) NULL DEFAULT NULL,\
                                `introduceText` VARCHAR(200) NULL DEFAULT NULL,\
                                `profileTotCnt` VARCHAR(50) NULL DEFAULT NULL,\
                                `profileTotInfo` VARCHAR(300) NULL DEFAULT NULL,\
                                `friendsCnt` VARCHAR(50) NULL DEFAULT NULL,\
                                `likePeopleCnt` VARCHAR(50) NULL DEFAULT NULL,\
                                `imgLikeCnt` VARCHAR(50) NULL DEFAULT NULL,\
                                `vodCnt` VARCHAR(50) NULL DEFAULT NULL,\
                                `picCnt` VARCHAR(50) NULL DEFAULT NULL,\
                                `tscore` VARCHAR(50) NULL DEFAULT NULL,\
                                `cscore` VARCHAR(50) NULL DEFAULT NULL,\
                                `mscore` VARCHAR(50) NULL DEFAULT NULL,\
                                PRIMARY KEY (`no_index`)\
                            )\
                            ENGINE=InnoDB\
                            ;"

        self.cursor.execute(create_table_query)
        self.connection.close()

    #str(ResultDict['해당월게시물개수']),  # thisMnthArticleCnt
    #str(ResultDict['전월게시물개수'])  # preMnthArticleCnt

    #INSERT facebook
    def insert_record_origin_version(self, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15, f16, f17,
                                     f18, f19, f20, f21, f22, f23, f24, f25, f26, f27, f28, f29, f30, f31, f32, f33, f34, f35, f36, f37, f38, f39, f40, f41, f42, f43, f44, f45,
                                     f46, f47, f48, f49, f50, f51, f52, f53):
        try:
            insert_command = "INSERT INTO facebook_crawled_just (" \
                             "userName, facebookUrl, basicInfo_tot, contctInfo_tot, websiteSnsInfo, " \
                             "introduceText, profileTotCnt, profileTotInfo, friendsCnt, likePeopleCnt, " \
                             "imgLikeCnt, vodCnt, picCnt, fb_tscore, fb_cscore, " \
                             "fb_mscore, detail_info, allFrndCnt,knowEachFrnd,latestAddFrnd," \
                             "univFrnd,homeFrnd,homeTwnFrnd,fllwerCnt,likeHobbyAllCnt," \
                             "movieLikeCnt,tvLikeCnt,musicLikeCnt,bookLikeCnt,sportsTemaLikeCnt," \
                             "foodPlaceCnt,appAndGamesCnt,visitedPlc,visitedCity,recentVisitPlc," \
                             "evntCnt,eventContents,sawItCnt,sawMovieCnt,sawMovieContentCnt," \
                             "sawMovieTitle,replyCnt,replyContents,articleLikeCnt,articleShareCnt," \
                             "avgReplyCnt,avgReplyAndReply,gdExpssCnt,avgGdExpssRate,aboutInfoCnt," \
                             "thisMnthArticleCnt,preMnthArticleCnt,arrangeYears) VALUES('" \
                             + f1 + "','" + f2 + "','" + f3 + "','" + f4 + "','" + f5 + "','" + f6 + "','"\
                             + f7 + "','" + f8 + "','" + f9 + "','" + f10 + "','" + f11 + "','" + f12 + "','"\
                             + f13 + "','" + f14 + "','" + f15 + "', '" + f16 + "', '" + f17 + "','"\
                             + f18 + "','" + f19 + "','" + f20 + "','" + f21 + "','" + f22 + "','" + f23 + "','" \
                             + f24 + "','" + f25 + "','" + f26 + "','" + f27 + "','" + f28 + "','" + f29 + "','" \
                             + f30 + "','" + f31 + "','" + f32 + "', '" + f33 + "', '" + f34 + "','" + f35 + "','" \
                             + f36 + "','" + f37 + "','" + f38 + "', '" + f39 + "', '" + f40 + "','" + f41 + "','" \
                             + f42 + "','" + f43 + "','" + f44 + "', '" + f45 + "', '" + f46 + "', '" + f47 + "', '" \
                             + f48 + "', '" + f49 + "', '" + f50 + "', '" + f51 + "', '" + f52 + "', '" + f53 + "' )"

            print(insert_command)
            self.cursor.execute(insert_command)
            self.connection.commit()
            self.connection.close()

        except Exception as e:
            print(e)






    #INSERT
    def insert_record_facebookInfo(self, f1, f2, f3, f4, f5, f6, f7):

        print('f4 :', f4)
        try:
            insert_command = "INSERT INTO facebook_crawled_just (" \
                             "userName, facebookUrl, basicInfo_tot, detail_info,  fb_tscore, fb_cscore, fb_mscore" \
                             ") VALUES('" \
                             + f1 + "','" + f2 + "','" + f3 + "','" + f4 + "','" + f5  + "','" + f6 + "','" + f7 +"')"

            print(insert_command)
            self.cursor.execute(insert_command)
            self.connection.commit()
            self.connection.close()

        except Exception as e:
            print(e)

    # UPDATE
    def update_ReviewCnt(self, f1, f2):
        print('update_ReviewCnt')
        try:
            insert_command = "UPDATE facebook_crawled_just SET " \
                        "reviewsCnt='" + f1 + "' WHERE facebookUrl='" + f2 + "'; "

            print(insert_command)
            self.cursor.execute(insert_command)
            self.connection.commit()

            print('DB insert of reviewsCnt success')
            self.connection.close()

        except Exception as e:
            print(e)

    # UPDATE
    def update_FollowerCnt(self, f1, f2):
        print('update_FollowerCnt')
        try:
            insert_command = "UPDATE facebook_crawled_just SET " \
                        "fllwCnt='" + f1 + "' WHERE facebookUrl='" + f2 + "'; "

            print(insert_command)
            self.cursor.execute(insert_command)
            self.connection.commit()

            print('DB insert of fllwCnt success')
            self.connection.close()

        except Exception as e:
            print(e)



    # UPDATE
    def update_PhotoLikeCmntCnt(self, f1, f2, f3):
        print('update_PhotoLikeCmntCnt')
        try:
            insert_command = "UPDATE facebook_crawled_just SET " \
                        "phdatgulCnt='" + f1 + "', photoLikeCnt='" + f2 + "' WHERE facebookUrl='" + f3 + "'; "

            print(insert_command)
            self.cursor.execute(insert_command)
            self.connection.commit()

            print('DB insert of update_PhotoLikeCmntCnt success')
            self.connection.close()

        except Exception as e:
            print(e)






