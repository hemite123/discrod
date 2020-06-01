import pymysql

connection = pymysql.connect(host="sql12.freemysqlhosting.net",user="sql12344778",passwd="KP46SK96Gv",database="sql12344778")
cursor = connection.cursor()

def GetBalance(self, id):
    retrive = "SELECT balance FROM user WHERE user_id = " + str(id)
    cursor.execute(retrive)
    rows = cursor.fetchone()
    return rows
    connection.commit()

def InputUser(self,id,name):
    insert = "INSERT INTO user(user_id,nickname,balance) VALUES('"+ str(id) + "','" + str(name)  +"', 0 );"
    cursor.execute(insert)
    connection.commit()

def CheckUser(self,id,act):
    retrive = "SELECT * FROM user WHERE user_id = " + str(id)
    cursor.execute(retrive)
    rows = cursor.fetchall()
    if act == "rcount":
        return cursor.rowcount
    else:
        return rows
    connection.commit()        

def UpdateUserPokemon(self,id,pokename):
    updateData = "UPDATE user SET pokestart='"+str(pokename)+"'WHERE user_id=" + str(id)
    cursor.execute(updateData)
    connection.commit()
    

