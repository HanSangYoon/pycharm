import pymysql
import self

class DatabaseConnection:
    def __init__(self):
        try:
            '''
            self.connection = pymysql.connect(host='127.0.0.1',
                       user='aster_dba', password='!sci716811',
                       db='aster_sci', charset='utf8')
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            '''
            self.connection = pymysql.connect(host='127.0.0.1',
                                              user='aster_dba', password='!sci716811',
                                              db='aster_sci', charset='utf8')
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()

            print('success')

        except:
            print('Cannot connect to Database')



    # INSERT
    def insert_profile_record(self):
        print('insert_profile_record')
        try:
            insert_command = "INSERT INTO aster_sci_tcm_tmp(fb_PageID, fb_userName, fb_user_introduce, " \
                             "fb_user_prfllen, fb_user_prflInfo, fb_insertTime) VALUES('han', 'sang', 'yoon', 'qwe', 'qweqwe', 'qweqweqweqwe')"

            print(insert_command)
            self.cursor.execute(insert_command)
            print('yoon')

            self.connection.commit()
            self.connection.close()

        except Exception as e:
            print(e)


if __name__ == '__main__':
    database_connection = DatabaseConnection()
    database_connection.insert_profile_record()