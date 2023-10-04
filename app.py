#general
#-------------------------------------------------------------------------#  
from flask import Flask,render_template,redirect,request,session,send_file, jsonify
import sqlite3,datetime,pandas
import random
from flask_cors import CORS


app = Flask(__name__)
CORS(app,headers='Content-Type')
app.secret_key = 'fghdfghdfgh'

def query (sql):
    with sqlite3.connect('users.db') as conn:
        cur=conn.cursor()
        rows = cur.execute(sql)
        return list(rows)


def users_data():
    rows = (query(f"SELECT * FROM users "))
    table =[]
    for row in rows:
        table.append({'name':row[0],'username':row[1],'password':row[2],'email':row[3],'team':row[4]})
    return table
users_table = users_data()




def items_data():
    rows = (query(f"SELECT * FROM items "))
    table =[]
    for row in rows:
        table.append({'mkt':row[0],'category':row[1],'item_name':row[2],'quantity':row[3],'added by':row[4],'entrance date':row[5],'updaating date':row[6]})
    return table
items_table = items_data()


def requests_data():
    rows = (query(f"SELECT * FROM requests "))
    table =[]
    for row in rows:
        table.append({'request number':row[0],'username':row[1],'email':row[2],'phone number':row[3],'items':row[4],'quantity':row[5],'taking date':row[6],'returning date':row[7]})
    return table
requests_table = requests_data()





#Users - login-register-homepage
#-------------------------------------------------------------------------#  
#homepage
@app.route('/')
def home():
    if session.get('username') == None:
        return redirect('/login')
    
    for user in users_table:
        if session.get('username') == user['username']:
            return render_template('home.html',username = session['username'])
    return redirect('/login')

#login
@app.route('/login', methods = ["POST",'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    for user in users_table:
        if ((request.form['username'] == user['username']) and (request.form['password'] == user['password'])):
            session['username'] = request.form['username'] 
            return redirect('/')
    
    return redirect('/register')

        
        

#register
@app.route('/register', methods = ["POST",'GET'])
def register():
    if users_table ==[]:
        query(f"INSERT INTO users VALUES('{request.form['name']}' ,'{request.form['username']}' , '{request.form['password']}' , '{request.form['phone']}' , '{request.form['email']}', '{request.form['team']}' )")
        session['username'] = request.form['username'] 
        return redirect('/')

    if request.method == 'GET':
        return render_template('register.html')
    
    new_user=request.form['username']
    for user in users_table:
        if new_user == user['username']:
            return render_template('register.html',users_table=users_table,new_user=new_user,message='This user is already exist')
        
    query(f"INSERT INTO users VALUES('{request.form['name']}' ,'{request.form['username']}' , '{request.form['password']}' , '{request.form['phone']}' , '{request.form['email']}', '{request.form.get('team')}' )")
    
    session['username'] = request.form['username'] 
    return redirect('/')


#users menu - admin
@app.route('/admin/users_menu')
def users_menu():
    if session.get('username') == 'admin':
        return render_template('users_menu.html')


#delete user
@app.route('/admin/users_menu/delete',methods = ['GET','POST'])
def delete_user():
    deleted_user = request.form.get('username')
    query(f"DELETE FROM users WHERE username='{deleted_user}'")
    
    return render_template('delete_user.html',users_table=users_table,deleted_user=deleted_user,message1 = 'No such user',message2 = 'User deleted')


with sqlite3.connect('users.db') as conn: 
    query1 = "SELECT * FROM users" 
    df = pandas.read_sql_query(query1, conn)
    df.to_csv('users.csv', index=False)
    
     

#items - add,update,delete,read
#--------------------------------------------------------------------------------#
#items menu
@app.route('/items')
def items():
    if session.get('username') != 'admin':
        return redirect('/')
    return render_template('items_menu.html')




#add items
@app.route('/items/add_items',methods = ['GET','POST'])
def get_items():
    if session.get('username') != 'admin':
        return redirect('/')
    
    for item in items_table:
        if request.form.get("mkt") == item["mkt"]:
           message1 = 'item is already exist'
           return render_template('add_items.html',message1=message1,switch=1)
        pass
           
    query(f"INSERT INTO items VALUES('{request.form.get('mkt')}', '{request.form.get('category')}', '{request.form.get('item_name')}', '{request.form.get('quantity')}','{request.form.get('quantity')}' ,'{request.form.get('added_by')}','{request.form.get('entrance_date')}','{datetime.datetime.now()}')")
    message2 = 'item added successfully'
    return render_template('add_items.html',message2=message2,switch=2)





#update items
@app.route('/admin/items/update', methods = ['GET','POST'])
def update_items():
    if session.get('username') != 'admin':
        return redirect('/')
           
   
    for item in items_table:
        if request.form.get('mkt') == item['mkt']:
            query(f"UPDATE items SET quantity= quantity +'{int(request.form.get('quantity'))}' WHERE mkt='{request.form.get('mkt')}'")
            query(f"UPDATE items SET quantity_in_stock = quantity_in_stock +'{int(request.form.get('quantity'))}' WHERE mkt='{request.form.get('mkt')}'")

    query(f"UPDATE items SET added_by='{request.form.get('added_by')}' WHERE mkt='{request.form.get('mkt')}'")
    query(f"UPDATE items SET updating_date='{datetime.datetime.now()}' WHERE mkt='{request.form.get('mkt')}'")
    return render_template('update_items.html')




@app.route('/admim/items/delete',methods = ['GET','POST'])
def delete_item():
    query(f"DELETE FROM items WHERE mkt='{request.form.get('mkt')}'")
    
    return render_template('delete_items.html')







#requests
#----------------------------------------------------------------------------------#

@app.route('/requests',methods = ['POST','GET'])
def requests():
   for user in users_table:
        if session.get('username') == user['username']:
            return render_template('requests.html')
        else:
            return redirect('/login')
        
# def request_number():
#     serial= '0'
#     for i in range(10):
#         number = random.randrange(1,10)
#         serial+=str(number)
#     for request in requests_table:
#         if request['request_number'] == serial:
#         try:
            
#     return serial



@app.route('/add_requests',methods = ['POST','GET'])
def add_requests():
   for user in users_table:
        if session.get('username') == user['username']:
            return render_template('add_requests.html')
        else:
            return redirect('/login')
        


# @app.route('/insert_requests',methods = ['POST','GET'])
# def insert_requests():
#     for request in requests_table:
#         query(f"INSERT INTO requests VALUES('{request_number()}','{session.get('username')},{}'")
#         query(f"UPDATE requests SET quantity_in_stock = quantity_in_stock +'{int(request.form.get('quantity'))}' WHERE mkt='{request.form.get('mkt')}'")

        

@app.route('/select_category', methods= ["GET"])
def add_item_request():
    chosen_categoey = request.form.get('category')
    rows = (query(f"SELECT mkt,\"item name\" FROM items WHERE category='{chosen_categoey}'"))
    items =[]
    for row in rows:
        items.append({'mkt':row[0],'item_name':row[1]})
    return jsonify(items)



    





#Exit
#----------------------------------------------------------------------------------#
@app.route('/exit')
def exit():
    session['username']= None
    return redirect('/login')





#admin
#----------------------------------------------------------------------------------#
@app.route('/admin')
def admin():
    if session.get('username') == 'admin':
        return render_template('admin.html')
    else:
        return render_template('admin_error.html')


#export items table to excel 
@app.route('/download_file',methods = ['GET','POST'])
def excel_items():
    with sqlite3.connect('users.db') as conn: 
        query1 = "SELECT * FROM items" 
        df = pandas.read_sql_query(query1, conn)
    df.to_excel('items.xlsx',index=False)
    return send_file(
        'items.xlsx',
        as_attachment=True,
        download_name='items_data.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )


#export users table to excel 
@app.route('/download_excel_users',methods = ['GET','POST'])
def excel_users():
    with sqlite3.connect('users.db') as conn: 
        query1 = "SELECT * FROM users" 
        df = pandas.read_sql_query(query1, conn)
    df.to_excel('users.xlsx',index=False)
    return send_file(
        'users.xlsx',
        as_attachment=True,
        download_name='users_data.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
