
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
'''
class DatabaseConnection:
    def __init__(self):
        try:
            self.connection = pymysql.connect(host='127.0.0.1',
                       user='aster_dba', password='!sci716811',
                       db='aster_sci', charset='utf8')
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()

            print('success connection to DB')

        except:
            print('Cannot connect to Database')

    def create_table(self):
        create_table_query = ""

        self.cursor.execute(create_table_query)
        self.connection.close()

    #INSERT
    def insert_profile_record(self, f1, f2, f3, f4, f5, f6):
        print('insert_profile_record')
        try:
            insert_command = "INSERT INTO aster_sci_tcm_tmp(fb_PageID, fb_userName, fb_user_introduce, " \
                             "fb_user_prfllen, fb_user_prflInfo, fb_insertTime) VALUES('" \
                             + f1 + "','" + f2 + "','" + f3 + "','" + f4 + "','" + f5 + "','" + f6 + "')"

            print(insert_command)
            self.cursor.execute(insert_command)
            print('yoon')

            self.connection.commit()
            self.connection.close()

        except Exception as e:
            print(e)


    def update_aboutInfo_record(self, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15, f16, f17, f18, f19, f20, f21, f22, f23, f24, f25, f26, f27, f28):
        print('yoonUp')
        #fb_about_vipEvt="+ f27 +" " \
        try:
            upodate_command = "UPDATE aster_sci_tcm_tmp SET " \
                                        "fb_about_spec_lgth='"+ f6 +"', " \
                                        "fb_about_spec='"+ f7 +"', " \
                                        "fb_about_work_lgth='"+ f8 +"', " \
                                        "fb_about_work='"+ f9 +"', " \
                                        "fb_about_edu_lgth='"+ f10 +"', " \
                                        "fb_about_edu='"+ f11 +"', " \
                                        "fb_about_hometwn='"+ f12 +"', " \
                                        "fb_about_live='"+ f13 +"', " \
                                        "fb_about_livetc='"+ f14 +"'," \
                                        "fb_about_cell='"+ f15 +"', " \
                                        "fb_about_webSns='"+ f16 +"', " \
                                        "fb_about_socialLink='"+ f17 +"', " \
                                        "fb_about_contactTotInfo='"+ f18 +"', " \
                                        "fb_about_bthLunar='"+ f19 +"', " \
                                        "fb_about_sex='"+ f20 +"', " \
                                        "fb_about_bloodTyp='"+ f21 +"', " \
                                        "fb_about_religion='"+ f22 +"', " \
                                        "fb_about_bscinf='"+ f23 +"', " \
                                        "fb_about_marrg='"+ f24 +"', " \
                                        "fb_about_family='"+ f25 +"', " \
                                        "fb_about_detltx='"+ f26 +"', " \
                                        "fb_about_facebookAddr='" + f27 + "' WHERE fb_PageID='" + f28 +"';"

            print(upodate_command)
            self.cursor.execute(upodate_command)
            self.connection.commit()

            print('DB Update success')
            self.connection.close()

        except Exception as e:
            print('DB UPDATE ERROR : ', e)

    #INSERT
    def update_tcm_score(self, f1, f2, f3, f4):

        print('update_tcm_score get in')

        try:
            insert_command = "UPDATE aster_sci_tcm_tmp SET sns_tscore='" + f1 + "', " \
                                                         "sns_cscore='" + f2 + "', " \
                                                         "sns_mscore='" + f3 + "' WHERE fb_PageID='" + f4 +"';"

            print(insert_command)
            self.cursor.execute(insert_command)
            self.connection.commit()

            print('SCORE DB Update success')
            self.connection.close()

        except Exception as e:
            print(e)

    def select_record(self):
        try:
            self.cursor.execute("SELECT * FROM aster879_tcmscore")
            cats = self.cursor.fetchall()
            for cat in cats:
                print("each rows : {}".format(cat))

            self.connection.close()
        except Exception as e:
            print(e)
'''


class DatabaseConnection_origin:
    def __init__(self):

        try:

            #SCI
            '''
            self.connection = pymysql.connect(host='172.16.4.158',
                       user='aster_sci_add', password='!sci716811',
                       db='aster_sci', charset='utf8')
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            '''
            '''
            #localhost
            self.connection = pymysql.connect(host='localhost',
                       user='aster_dba', password='!sci716811',
                       db='aster_sci', charset='utf8')
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            
            
                        #localhost
            self.connection = pymysql.connect(host='localhost',
                       user='aster_dba', password='!sci716811',
                       db='aster', charset='utf8')

            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            '''

            #localhost
            self.connection = pymysql.connect(host='uml.kr', port=3366,
                       user='aster_dba', password='!aster716811',
                       db='aster', charset='utf8')

            self.connection.autocommit = True
            self.cursor = self.connection.cursor()


            print('DB connection completed')

        except:
            print('Cannot connect to Database')

    def create_table(self):
        create_table_query = "CREATE TABLE `aster_sci_tcm` (\
	`no_index` INT(11) NOT NULL AUTO_INCREMENT,\
	`insertedTime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,\
	`cellPhone` VARCHAR(50) NULL DEFAULT NULL,\
	`facebookUrl` VARCHAR(50) NULL DEFAULT NULL,\
	`kks_pageID` VARCHAR(50) NULL DEFAULT NULL,\
	`naverblogID` VARCHAR(50) NULL DEFAULT NULL,\
	`ins_pageID` VARCHAR(50) NULL DEFAULT NULL,\
	`userName` VARCHAR(50) NULL DEFAULT NULL,\
	`birthday` VARCHAR(50) NULL DEFAULT NULL,\
	`birthday_luna` VARCHAR(50) NULL DEFAULT NULL,\
	`sex` VARCHAR(50) NULL DEFAULT NULL,\
	`bloodType` VARCHAR(50) NULL DEFAULT NULL,\
	`addr` VARCHAR(100) NULL DEFAULT NULL,\
	`basicInfo_tot` VARCHAR(500) NOT NULL,\
	`contctInfo_tot` VARCHAR(500) NOT NULL,\
	`websiteSnsInfo` VARCHAR(1000) NOT NULL,\
	`website` VARCHAR(50) NULL DEFAULT NULL,\
	`snsLink` VARCHAR(50) NULL DEFAULT NULL,\
	`religion` VARCHAR(50) NULL DEFAULT NULL,\
	`introduceText` VARCHAR(200) NULL DEFAULT NULL,\
	`profileTotCnt` VARCHAR(50) NULL DEFAULT NULL,\
	`profileTotInfo` VARCHAR(1000) NULL DEFAULT NULL,\
	`friendsCnt` VARCHAR(50) NULL DEFAULT NULL,\
	`likePeopleCnt` VARCHAR(50) NULL DEFAULT NULL,\
	`imgLikeCnt` VARCHAR(50) NULL DEFAULT NULL,\
	`vodCnt` VARCHAR(50) NULL DEFAULT NULL,\
	`picCnt` VARCHAR(50) NULL DEFAULT NULL,\
	`kks_nickNm` VARCHAR(50) NULL DEFAULT NULL,\
	`kk_strCnt` VARCHAR(50) NULL DEFAULT NULL,\
	`kk_bthday` VARCHAR(50) NULL DEFAULT NULL,\
	`kk_eduNm` VARCHAR(50) NULL DEFAULT NULL,\
	`kk_fvrMusic` VARCHAR(50) NULL DEFAULT NULL,\
	`kk_liveNow` VARCHAR(50) NULL DEFAULT NULL,\
	`kk_workNow` VARCHAR(50) NULL DEFAULT NULL,\
	`nb_articlecnt` VARCHAR(50) NULL DEFAULT NULL,\
	`nb_todayVisit` VARCHAR(50) NULL DEFAULT NULL,\
	`nb_totalVisit` VARCHAR(50) NULL DEFAULT NULL,\
	`nb_articlewordCnt` VARCHAR(50) NULL DEFAULT NULL,\
	`ins_ArticlCnt` VARCHAR(50) NULL DEFAULT NULL,\
	`ins_fllwrCnt` VARCHAR(50) NULL DEFAULT NULL,\
	`ins_flwingCnt` VARCHAR(50) NULL DEFAULT NULL,\
	`ins_ArtWrdCnt` VARCHAR(50) NULL DEFAULT NULL,\
	`ins_hstgCnt` VARCHAR(50) NULL DEFAULT NULL,\
	`fb_tscore` VARCHAR(50) NULL DEFAULT NULL,\
	`fb_cscore` VARCHAR(50) NULL DEFAULT NULL,\
	`fb_mscore` VARCHAR(50) NULL DEFAULT NULL,\
	`kk_tscore` VARCHAR(50) NULL DEFAULT NULL,\
	`kk_cscore` VARCHAR(50) NULL DEFAULT NULL,\
	`kk_mscore` VARCHAR(50) NULL DEFAULT NULL,\
	`nb_tscore` VARCHAR(50) NULL DEFAULT NULL,\
	`nb_cscore` VARCHAR(50) NULL DEFAULT NULL,\
	`nb_mscore` VARCHAR(50) NULL DEFAULT NULL,\
	`tot_tscore` VARCHAR(50) NULL DEFAULT NULL,\
	`tot_cscore` VARCHAR(50) NULL DEFAULT NULL,\
	`tot_mscore` VARCHAR(50) NULL DEFAULT NULL,\
	`userSnsRank` VARCHAR(50) NULL DEFAULT NULL,\
	`search_start_date` DATE NULL DEFAULT NULL,\
	`search_end_date` DATE NULL DEFAULT NULL,\
	PRIMARY KEY (`no_index`),\
	UNIQUE INDEX `UNIQUE KEY` (`facebookUrl`),\
	UNIQUE INDEX `cellPhone` (`cellPhone`)\
)\
COLLATE='utf8_general_ci'\
ENGINE=InnoDB\
ROW_FORMAT=DYNAMIC\
;\
"

        self.cursor.execute(create_table_query)
        self.connection.close()

    #INSERT,SELECT
    def pre_Insert_sci_record(self):
        try:
            insertedId = ''
            self.cursor.execute("INSERT INTO syhan_queue (syhan_queue.search_log_index) "\
                                                        "SELECT search_log.search_log_index "\
                                                        "FROM search_log "\
                                                        "WHERE search_log.search_log_flag='DVO' AND search_log.search_log_index > ( "\
                                                        "SELECT syhan_queue.search_log_index "\
                                                        "FROM syhan_queue "\
                                                        "ORDER BY syhan_queue.search_log_index DESC "\
                                                        "LIMIT 0,1 "
                                                        ") "\
                                                        "ORDER BY search_log.search_log_index "\
                                                        "LIMIT 0,1;"
                            )

            insertedId = self.connection.insert_id()
            print('insertedId type : ',type(insertedId))
            print('insertedId : ', insertedId)

            self.connection.commit()

            self.cursor.execute("SELECT search_log_index FROM syhan_queue WHERE seq_indexNo=" + str(insertedId).replace(" ", ""))
            returnResult = self.cursor.fetchone()

            str(''.join(str(returnResult[0])))

            #select_sci_record()를 실행해야 하기 때문에 connection이 끊어지면 안됨.
            #self.connection.close()
            return returnResult

        except Exception as e:
            print(e)


    #상단의 pre_Insert_sci_record 함수를 통해서 취득한 search_log 테이블의 search_log_index값을 가지고
    #SELECT
    def select_lastIndex_sci_record(self, searchIdx):
        try:
            select_Query ="SELECT search_log_index, search_log_real_name " \
                          "FROM search_log " \
                          "WHERE search_log_flag='DVO' AND search_log_index='"+ searchIdx +"';"
            print(select_Query)
            self.cursor.execute(select_Query)
            cats = self.cursor.fetchall()

            for cat2 in cats:
                print(cat2)
                return cat2
            self.connection.close()
        except Exception as e:
            print(e)

    #
    #SELECT
    def select_sci_record(self, searchIdx):

        #search_log_from_date,  search_log_to_date
        try:
            select_Query ="SELECT search_log_mobile, search_log_kakaostory_url, search_log_naver_blog_url, search_log_facebook_url, search_log_real_name, search_log_from_date, search_log_to_date " \
                          "FROM search_log " \
                          "WHERE search_log_flag='DVO' AND search_log_index='"+ searchIdx +"';"
            print(select_Query)
            self.cursor.execute(select_Query)
            cats = self.cursor.fetchall()

            for cat in cats:
                print('cat :', cat)

                return cat

            self.connection.close()
        except Exception as e:
            print(e)



    #INSERT facebook
    def insert_record_origin_version(self, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15, f16, f17):
        try:
            insert_command = "INSERT INTO aster_sci_tcm (" \
                             "userName, facebookUrl, cellPhone, basicInfo_tot, contctInfo_tot, websiteSnsInfo, " \
                             "introduceText, profileTotCnt, profileTotInfo, friendsCnt, likePeopleCnt, " \
                             "imgLikeCnt, vodCnt, picCnt, fb_tscore, fb_cscore, fb_mscore" \
                             ") VALUES('" \
                             + f1 + "','" + f2 + "','" + f3 + "','" + f4 + "','" + f5  + "','" + f6 + "','"\
                             + f7 + "','" + f8 + "','" + f9 + "','" + f10 + "','" + f11 + "','" + f12 + "','"\
                             + f13 + "','" + f14 + "','" + f15 + "', '" + f16 + "', '" + f17 + "')"

            print(insert_command)
            self.cursor.execute(insert_command)
            self.connection.commit()
            self.connection.close()

        except Exception as e:
            print(e)


    # UPDATE kakaostory
    def update_kakaoStoryRecord(self, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12):
        print('update_kakaoStoryRecord')
        try:
            insert_command = "UPDATE aster_sci_tcm SET " \
                        "kks_pageID='" + f1 + "', " \
                        "kks_nickNm='" + f2 + "', " \
                        "kk_strCnt='" + f3 + "', " \
                        "kk_bthday='" + f4 + "', " \
                        "kk_eduNm='" + f5 + "', " \
                        "kk_fvrMusic='" + f6 + "', " \
                        "kk_liveNow='" + f7 + "', " \
                        "kk_workNow='" + f8 + "', " \
                        "kk_tscore='" + f9 + "', " \
                        "kk_cscore='" + f10 + "', " \
                        "kk_mscore='" + f11 + "' WHERE cellPhone='" + f12 + "'; "

            print(insert_command)
            self.cursor.execute(insert_command)
            self.connection.commit()

            print('DB insert of Kakao success')
            self.connection.close()

        except Exception as e:
            print(e)



    # UPDATE naverblog
    def update_naverblogRecord(self, f1, f2, f3, f4, f5, f6, f7, f8, f9):
        print('update_instagramRecord')
        try:
            insert_command = "UPDATE aster_sci_tcm SET " \
                        "naverblogID='" + f1 + "', " \
                        "nb_articlecnt='" + f2 + "', " \
                        "nb_todayVisit='" + f3 + "', " \
                        "nb_totalVisit='" + f4 + "', " \
                        "nb_articlewordCnt='" + f5 + "', " \
                        "nb_tscore='" + f6 + "', " \
                        "nb_cscore='" + f7 + "', " \
                        "nb_mscore='" + f8 + "' WHERE cellPhone='" + f9 + "'; "

            print(insert_command)
            self.cursor.execute(insert_command)
            self.connection.commit()

            print('DB insert of naverblog DATA success')
            self.connection.close()

        except Exception as e:
            print(e)


    # UPDATE instagram
    def update_instagramRecord(self, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10):
        print('update_instagramRecord')
        try:
            insert_command = "UPDATE aster_sci_tcm SET " \
                        "ins_pageID='" + f1 + "', " \
                        "ins_ArticlCnt='" + f2 + "', " \
                        "ins_fllwrCnt='" + f3 + "', " \
                        "ins_flwingCnt='" + f4 + "', " \
                        "ins_ArtWrdCnt='" + f5 + "', " \
                        "ins_hstgCnt='" + f6 + "', " \
                        "ins_tscore='" + f7 + "', " \
                        "ins_cscore='" + f8 + "', " \
                        "ins_mscore='" + f9 + "' WHERE cellPhone='" + f10 + "'; "

            print(insert_command)
            self.cursor.execute(insert_command)
            self.connection.commit()

            print('DB insert of instagram DATA success')
            self.connection.close()

        except Exception as e:
            print(e)


    # UPDATE tcm score
    def update_totalTCM_Record(self, f1, f2, f3, f4, f5, f6, f7, f8):

        '''
            str(tot_TSCORE),
            str(tot_CSCORE),
            str(tot_MSCORE),
            userSNSRank,
            fromDate,
            toDate,
            userCellPhNum,
            userName
        '''
        print('update_totalTCM_Record')
        try:
            update_command = "UPDATE aster_sci_tcm SET " \
                        "tot_tscore='" + f1 + "', " \
                        "tot_cscore='" + f2 + "', " \
                        "tot_mscore='" + f3 + "', " \
                        "userSnsRank='" + f4 + "', " \
                        "user_real_name='" + f8 + "', " \
                        "search_start_date='" + f5 + "', " \
                        "search_end_date='" + f6 + "' WHERE cellPhone='" + f7 + "'; "

            print(update_command)
            self.cursor.execute(update_command)
            self.connection.commit()

            insert_command = "INSERT INTO aster_tcm_totalinfo(real_name, cellPhone, t_score, c_score, m_score, user_rank) VALUES (" \
                             "'" + f8 + "', '" + f7 + "', '" + f1 +"', '" + f2 + "', '" + f3 + "', '" + f4 + "' );"

            print(insert_command)
            self.cursor.execute(insert_command)
            self.connection.commit()


            print('DB insert of Total TCM DATA success')
            self.connection.close()

        except Exception as e:
            print(e)



