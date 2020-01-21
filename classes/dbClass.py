# database 
# ver 1.2

import os
import MySQLdb
import time
import datetime
import pipes
import mysql.connector

class DbClassTable():
    
    def __init__(self,name,dataPath,dbname,tablename,sqltxt,host,user,psw):
        print("DbClassTable initalization")
        self.dbName = dbname
        self.tablename = tablename
        self.Info = {}
        self.init_Info(name)
        self.setInfo(1,host,user,psw,dbname)
        self.pathName  = dataPath+name+"Values.txt"
        print("self.pathName "+self.pathName)
        self.getDbInfoToFile()
        if (self.Info["flag"]==1):
            #try:
            self.connOpen()
            self.createDB(self.dbName)
            self.createTable(sqltxt)
            self.connClose()
            #except:
            #    self.Info["flag"]=0
    def init_Info(self,name):
        self.Info["name"] = name
        self.Info["flag"] = 0
        self.Info["host"] = ""
        self.Info["user"] = ""
        self.Info["password"] = ""
    def setInfo(self,flag,host,user,psw,dbName):
        print("setInfo")
        self.Info["flag"] = flag
        self.Info["host"] = host
        self.Info["user"] = user
        self.Info["password"] = psw
        try:
            self.connOpen()
            print("connection opened")
            #self.setDbInfoToFile(self.Info)
            #print("file saved")
        except:
            self.Info["host"] = ""
            self.Info["user"] = ""
            self.Info["password"] = ""
    def setDbInfoToFile(self,dbInfo):
        try:
            os.chmod(self.pathName,0o666)
        except:
            pass
        f= open(self.pathName,"w+")
        f.write("flag %d\r\n" % (dbInfo["flag"]))
        f.write("host %s\r\n" % (dbInfo["host"]))
        f.write("user %s\r\n" % (dbInfo["user"]))
        f.write("password %s\r\n" % (dbInfo["password"]))
        f.close() 
        #win32api.SetFileAttributes(path,win32con.FILE_ATTRIBUTE_HIDDEN)
    def getDbInfoToFile(self):
        try:
            os.chmod(self.pathName,0o666)
            with open(self.pathName,"r") as ins:
                for line in ins:
                    #print(line)
                    if(line[0:4]=="flag"):
                        self.Info["flag"] = int(line[5])
                    if(line[0:4]=="host" ):
                        self.Info["host"] = line[5:-1]
                    if(line[0:4]=="user"):
                        self.Info["user"] = line[5:-1]
                    if(line[0:8]=="password"):
                        self.Info["password"] = line[9:-1]
        except:
            return 0
    def connOpen(self):
        # Open database connection
        #print("connOpen")
        #print(self.Info)
        self.conn = MySQLdb.connect(self.Info["host"],self.Info["user"],self.Info["password"] )
        #print("prepare a cursor object using cursor() method")
        # prepare a cursor object using cursor() method
        self.cursor = self.conn.cursor()
    def connClose(self):
        # disconnect from server
        self.conn.close()
    def createDB(self,name):
        try:
            self.useDb(name)
        except MySQLdb.OperationalError:
            sql = "CREATE DATABASE {db}"
            self.cursor.execute(sql.format(db=name))
            self.useDb(name)
    def useDb(self,name):
        sql = "USE {db}"
        qry = self.cursor.execute(sql.format(db=name))
    def createTable(self,sqltxt):
        print("createTable")
        name = self.tablename
        print("name table "+name)
        sql = "SHOW TABLES"
        qry = self.cursor.execute(sql)
        results= self.cursor.fetchall()
        flag_db = False
        if results:
            for result in results:
                if result[0]==name:
                    flag_db = True
                    print("not has to create")
        print(flag_db)
        if not flag_db:
            sql = """
            CREATE TABLE IF NOT EXISTS {table} (
                {sql_body}
                )
            """
            qry = self.cursor.execute(sql.format(table=name,sql_body=sqltxt))
            sql = """
            ALTER TABLE {table} ADD COLUMN id int NOT NULL AUTO_INCREMENT PRIMARY KEY
            """
            qry = self.cursor.execute(sql.format(table=name))
            self.conn.commit()
        print("createTable end")
    def selectTable(self):
        self.connOpen()
        self.useDb(self.dbName)
        sql = """SELECT * FROM {table}"""
        self.cursor.execute(sql.format(table=self.tablename))
        rows = self.cursor.fetchall()
        self.conn.commit()
        self.connClose()
        return rows
    def selectTableId(self,id_):
        self.connOpen()
        self.useDb(self.dbName)
        data = [
            id_,
        ]
        sql = """SELECT * FROM {table} WHERE id=%s"""
        self.cursor.execute(sql.format(table=self.tablename),data)
        row = self.cursor.fetchone()
        self.conn.commit()
        self.connClose()
        return row
    def selectTablePart(self,fields,where):
        self.connOpen()
        self.useDb(self.dbName)
        sql = """SELECT {fields} FROM {table}"""
        self.cursor.execute(sql.format(fields=fields,table=self.tablename+" "+where))
        rows = self.cursor.fetchall()
        self.conn.commit()
        self.connClose()
        return rows
    def insertRow(self,data,sqltxt):
        self.connOpen()
        self.useDb(self.dbName)
        sql = """INSERT INTO {table}
        {sql_body}"""
        self.cursor.execute(sql.format(table=self.tablename,sql_body=sqltxt),data)
        self.conn.commit()
        self.connClose()
    def insertElement(self,value,sqltxt):
        self.connOpen()
        self.useDb(self.dbName)
        sql = "INSERT INTO {table} ({sql_body}) VALUES ({value})"
        self.cursor.execute(sql.format(table=self.tablename,sql_body=sqltxt,value=value))
        self.conn.commit()
        self.connClose()
    def updateTable(self,ids,data,sqltxt): 
        self.connOpen()
        self.useDb(self.dbName)
        data.append(ids)
        sql = """UPDATE {table} SET
        {bodysql}
        WHERE
        id=%s"""
        self.cursor.execute(sql.format(table=self.tablename,bodysql=sqltxt),data)
        self.conn.commit()
        self.connClose()
    def deleteRowByID(self,value): 
        self.connOpen()
        self.useDb(self.dbName)
        data = [
            value,
        ]
        sql = "DELETE FROM {table} WHERE id=%s"
        self.cursor.execute(sql.format(table=self.tablename),data)
        self.conn.commit()
        self.connClose()
    def getDbStatus(self):
        try:
            self.connOpen()
            return self.Info["flag"]
        except:
            return 0
    def copyTable(self,new_tableName,tableToCopy):
        self.connOpen()
        #self.useDb(self.dbName)
        new_tableName = self.dbName+"."+new_tableName
        tableToCopy = "doceye."+tableToCopy
        sql = """
        CREATE TABLE {new_table} 
        SELECT * 
        FROM
            {existing_table};
        """
        #print(sql.format(new_table=new_tableName,existing_table=tableToCopy))
        self.cursor.execute(sql.format(new_table=new_tableName,existing_table=tableToCopy))

        self.conn.commit()
        self.connClose()
    def exportTableToCsv(self,folderPath):
        self.connOpen()
        self.useDb(self.dbName)
        sql = """describe {table} """
        self.cursor.execute(sql.format(table=self.tablename))
        rows = self.cursor.fetchall()
        labels = ""
        for field in rows:
            if not field[0]=="path_1" or not field[0]=="path_2":
                labels += field[0]+", "
        #print(labels)
        labels += "\n"
        sql = """select * from {table} """
        self.cursor.execute(sql.format(table=self.tablename))
        rows = self.cursor.fetchall()
        body = ""
        for row in rows:
            for field in row:
                try:
                    body += field.strftime('%m/%d/%Y')+", "
                except:
                    body += str(field)+", "
            body += "\n"
        #print(body)
        f= open(folderPath+"/"+self.tablename+".csv","w+")
        f.write(labels)
        f.write(body)
        f.close() 
        self.conn.commit()
        self.connClose()
    def exportDb(self,folderPath):
        DATETIME = time.strftime('%Y%m%d-%H%M%S')
        path = folderPath+"/"+self.tablename+ DATETIME+".sql"
        current_path = os.getcwd()
        new_path = "C:\Program Files\MySQL\MySQL Server 5.7\\bin"
        os.chdir(new_path)
        os.system("mysqldump.exe --user=%s --password=%s --host=%s --port=3306 --result-file=%s --databases %s"%  (self.Info["user"],self.Info["password"],self.Info["host"],path,self.dbName))
        os.chdir(current_path)
    def importDb(self,sqlname):
        self.connOpen()
        self.useDb(self.dbName)
        # Open and read the file as a single buffer
        fd = open(sqlname, 'r')
        sqlFile = fd.read()
        fd.close()

        # all SQL commands (split on ';')
        sqlCommands = sqlFile.split(';')

        # Execute every command from the input file
        for command in sqlCommands:
            # This will skip and report errors
            # For example, if the tables do not yet exist, this will skip over
            # the DROP TABLE commands
            if command.rstrip() != '':
                    self.cursor.execute(command)
            try:
                if command.rstrip() != '':
                    self.cursor.execute(command)
            except:
                print("One command skipped")
        self.conn.commit()
        self.connClose()
    def altertable(self,field,type):
        name = self.tablename
        self.connOpen()
        self.useDb(self.dbName)
        try:
            sql = """
            SELECT {field} FROM {table}
            """
            qry = self.cursor.execute(sql.format(table=name,field=field))
            results= self.cursor.fetchall()
        except:
            sql = """
            ALTER TABLE {table} ADD COLUMN {field} {type}
            """
            qry = self.cursor.execute(sql.format(table=name,field=field,type=type))
            self.conn.commit()
            print("column added")
        self.conn.commit()
        self.connClose()