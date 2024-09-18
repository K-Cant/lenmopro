import pymysql

def getDBConnection():
    connection = pymysql.connect(
        host='localhost',         
        user='root',    
        password='password1', 
        database='libros'  
    )
    return connection