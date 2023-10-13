import sqlite3
import bcrypt

con = sqlite3.connect("database.db", check_same_thread=False)


def insert_user(username, email, password, rol):
    try:
        with con:
            cur=con.cursor()
            data=[
                (username),
                (email),
                (password),
                (rol)
            ]
            cur.execute("INSERT INTO users VALUES(?, ?, ?, ?)", data)
            con.commit()
        return True  
    except:
        return False
        
def get_user(username):
    """
        Input:
            username
        Output:
            a dictionary with the username, email, and role
    """
    data=[(username),] #format to read the query
    result=[]
    with con:
        cur=con.cursor()
        user_info=cur.execute("Select * from users where user_name=?", data)
        result=user_info.fetchone()
        con.commit()
    if result != None:
        user = {
                "username": result[0],
                "email": result[1],
                "role": result[3]
            }
        return user
    else:
        return None
    
def check_password(username: str, password: str) -> bool:
    """
        Check the validity of the entered password
        Input:
            username
            password
        Output:
            bool
            The validity of the entered password 
            by comparing it to the hashed password on database
    
    """
    data=[(username),] #format to read the query
    result=[]
    with con:
        cur=con.cursor()
        user_info=cur.execute("Select password from users where user_name=?", data)
        result=user_info.fetchone()
        con.commit()

    hashed=result[0]  
    if result != None:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    else:
        return False


def update_password(username, new_password):
    result=[]
    with con:
        cur=con.cursor()
        cur.execute("""Update users set password=? where user_name=?""", (new_password, username))
        con.commit()
    if result != None:
        return True
    else:
        return False

    

#maybe it is unnecessary
"""def fetch_all_users():
    result=[]
    result_dic=[]
    with con:
        cur=con.cursor()
        user_info=cur.execute("Select * from users")
        result=user_info.fetchall()
        con.commit()
    
    for tupla in result:
        diccionario = {
            "key": tupla[0],
            "email": tupla[1],
            "password": tupla[2],
            "role": tupla[3]
        }
        result_dic.append(diccionario)

    return result_dic"""
