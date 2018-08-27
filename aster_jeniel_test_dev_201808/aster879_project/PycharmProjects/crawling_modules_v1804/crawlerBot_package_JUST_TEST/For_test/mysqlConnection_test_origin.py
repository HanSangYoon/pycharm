
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


class DatabaseConnection:
    def __init__(self):

        try:
            self.connection = pymysql.connect(host='127.0.0.1',
                       user='root', password='1234',
                       db='just_jeniel', charset='utf8')
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()

        except:
            print('Cannot connect to Database')

    def create_table(self):
        create_table_query = "CREATE TABLE crawled_worknet_syhan (\
                                    no_index INT NOT NULL AUTO_INCREMENT COMMENT 'index',\
                                    articleUniqueNum VARCHAR(50) NOT NULL DEFAULT '0' COMMENT '구인인증번호',\
                                    corpNm VARCHAR(50) NOT NULL DEFAULT '0' COMMENT '리스트상의 회사이름',\
                                    corpWantJob VARCHAR(50) NOT NULL DEFAULT '0' COMMENT '리스트상의 공고내용(제목이 포함될 수 있음)',\
                                    corpRecruitArticleTitle VARCHAR(50) NOT NULL DEFAULT '0' COMMENT '리스트상의 공고제목',\
                                    searchArticleCnt VARCHAR(50) NOT NULL DEFAULT '0' COMMENT '공고조회수',\
                                    PRIMARY KEY(no_index, articleUniqueNum)\
                                )\
                                COLLATE='utf8_general_ci'\
                            ;"

        self.cursor.execute(create_table_query)
        self.connection.commit()
        self.connection.close()

    def insert_new_record(self, f1, f2, f3, f4 ,f5):
        try:
            #new_record = (f1, f2, f3, f4, f5)

            insert_command = "INSERT INTO crawled_worknet_syhan (articleUniqueNum) VALUES ('" + f1  + "'); "

            print(insert_command)
            self.cursor.execute(insert_command)
            self.connection.commit()
            self.connection.close()

        except Exception as e:
            print(e)


    def update_record(self, f1):
        try:
            #new_record = (f1, f2, f3, f4, f5)

            update_command = "UPDATE crawled_worknet_syhan SET articleUniqueNum ='" + f1  + "' WHERE no_index=27;"

            print(update_command)
            self.cursor.execute(update_command)

            self.connection.commit()
            self.connection.close()

        except Exception as e:
            print(e)

    def query_all(self):
        try:
            print('1')

            self.cursor.execute("select * from crawled_worknet_syhan;")
            print('2')
            cats = self.cursor.fetchall()
            print('3')
            for cat in cats:
                #print('cat', cat)
                print("each rows : {}".format(cat))

            self.connection.close()
        except Exception as e:
            print('123123-> ', e)

if __name__ == '__main__':


    try:
        database_connection = DatabaseConnection()
    except Exception as e1:
        print('1-->', e1)

    '''
    try:
        database_connection.create_table()
    except Exception as e2:
        print('2-->', e2)
    '''
    try:
        database_connection = DatabaseConnection()
        database_connection.insert_new_record('hoho', '@', '#', '$', '%')
    except Exception as e3:
        print('3-->', e3)

    '''
    try:
        database_connection = DatabaseConnection()
        database_connection.update_record('한상윤gkstkddbs')
    except Exception as e3_5:
        print(e3_5)

    '''
    try:
        database_connection = DatabaseConnection()
        database_connection.query_all()
    except Exception as e4:
        print('4-->', e4)
