import psycopg2
import datetime

#EX:
#insert_data.insert_usr(curs,conn,'xX_BigChungus_Xx','test@gmail.com','SQL','Big','Chungus',datetime.datetime(2020, 10, 16, 14, 17, 51, 720507),datetime.datetime(2020, 12, 16, 14, 17, 51, 720507))


def insert_usr(curs,conn,username,email,password,firstname,lastname,creationdate,lastaccessdate):
    """ create tables in the PostgreSQL database"""
    command = """
               INSERT INTO usr(username,email,password,firstname,lastname,creationdate,lastaccessdate)
                   VALUES(%s,%s,%s,%s,%s,%s,%s)
               """

    try:
        #for command in commands:
        print(command)
        curs.execute(command,(username,email,password,firstname,lastname,creationdate,lastaccessdate))
    except (Exception,psycopg2.DatabaseError) as error:
        print(error)