import sqlite3
import bcrypt

def insert_user(username, email, password, rol):
    con = sqlite3.connect("database.db", check_same_thread=False)
    #try:
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
                    # Close the cursor and the connection
    # Close the cursor and the connection    
    cur.close()
    con.close()
    return True  
    """except:
        return False"""
        
def get_user(username):
    """
        Input:
            username
        Output:
            a dictionary with the username, email, and role
    """
    con = sqlite3.connect("database.db", check_same_thread=False)
    data=[(username),] #format to read the query
    result=[]
    with con:
        cur=con.cursor()
        user_info=cur.execute("Select * from users where user_name=?", data)
        result=user_info.fetchone()
        con.commit()
    cur.close()
    con.close()
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
    con = sqlite3.connect("database.db", check_same_thread=False)
    data=[(username),] #format to read the query
    result=[]
    with con:
        cur=con.cursor()
        user_info=cur.execute("Select password from users where user_name=?", data)
        result=user_info.fetchone()
        con.commit()

    hashed=result[0] 
    # Close the cursor and the connection    
    cur.close()
    con.close() 
    if result != None:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    else:
        return False


def update_password(username, new_password):
    
    con = sqlite3.connect("database.db", check_same_thread=False)
    result=[]
    with con:
        cur=con.cursor()
        cur.execute("""Update users set password=? where user_name=?""", (new_password, username))
        con.commit()
    # Close the cursor and the connection    
    cur.close()
    con.close()
    if result != None:
        return True
    else:
        return False
