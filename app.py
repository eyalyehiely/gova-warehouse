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
        table.append({'request number':row[0],'username':row[1],'items':row[2],'quantity':row[3],'taking date':row[4],'returning date':row[5]})
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
            return render_template('register.html')
        
    query(f"INSERT INTO users VALUES('{request.form['name']}' ,'{request.form['username']}' , '{request.form['password']}' , '{request.form['phone']}' , '{request.form['email']}', '{request.form.get('team')}' )")
    
    session['username'] = request.form['username'] 
    return redirect('/')



#requests
#----------------------------------------------------------------------------------#

@app.route('/requests',methods = ['POST','GET'])
def requests():
    #checking validation & return template
   for user in users_table:
        if session.get('username') == user['username']:
            return render_template('requests.html')
        else:
            return redirect('/login')
        
def create_request_number():
    try:
        starter_number= '#'
        request_number = None
        for i in range(10):
            number = random.randrange(1,10)
            starter_number+=str(number)
        request_number= starter_number        
        return request_number
    except:
        if request_number == query(f"SELECT request_number FROM requests WHERE request_number='{request_number}'"):
            random.shuffle(request_number)
        return str(request_number)




#checking validation & return template
@app.route('/add_requests',methods = ['POST','GET'])
def add_requests():
   
   for user in users_table:
        if session.get('username') == user['username']:
            return render_template('add_requests.html')
        else:
            return redirect('/login')
        


 #add request to db & updates the tables
@app.route('/insert_requests',methods = ['POST','GET'])
def insert_requests():
    try:
        request_number=create_request_number()
        username= session.get('username')
        quantity = request.form.get('quantity')
        items = request.form['Item']
        taking_date = request.form.get('taking_date')
        returning_date =request.form.get('returning_date')
        status = "not approved"
        query(f"INSERT INTO requests VALUES('{request_number}', '{username}','{items}', '{quantity}', '{taking_date}', '{returning_date}','{status}','{datetime.datetime.today()}')")
        query(f"UPDATE items SET quantity_in_stock = quantity_in_stock - '{int(quantity)}' WHERE item_name ='{request.form.get('Item')}'") 
        return render_template('add_requests.html')   
    except:
        return "item not available" 



#return all items in stock
@app.route('/send_item_instock', methods= ["GET"])
def send_item_instock():
    chosen_item = request.args.get('Item')
    rows =(query(f"SELECT quantity_in_stock FROM items WHERE item_name='{chosen_item}'"))
    items_instock =[]
    for row in rows:
        items_instock.append({'item_name':row[0],'quantity_in_stock':row[1]})   
    return jsonify(items_instock)



#return all items per category
@app.route('/select_category', methods= ["GET"])
def add_item_request():
    chosen_category = request.args.get('category')
    rows = query(f"SELECT mkt,item_name FROM items WHERE category='{chosen_category}'")
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





#Superuser
#----------------------------------------------------------------------------------#
@app.route('/admin')
def admin():
    if session.get('username') == 'admin':
        return render_template('admin.html')
    else:
        return render_template('admin_error.html')
    


# - user
#----------------------------------------------------------------------------------#

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
    
    return render_template('delete_user.html')



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

#items
#-------------------------------------------------------------------------------------#

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
    
    # for item in items_table:
    #     if request.form.get("mkt") == item["mkt"]:
    #        return render_template('add_items.html')
        
           
    query(f"INSERT INTO items VALUES('{request.form.get('mkt')}', '{request.form.get('category')}', '{request.form.get('item_name')}', '{request.form.get('quantity')}','{request.form.get('quantity')}' ,'{request.form.get('added_by')}','{request.form.get('entrance_date')}','{datetime.datetime.now()}')")
    return render_template('add_items.html')





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



#delete_item from db
@app.route('/admim/items/delete',methods = ['GET','POST'])
def delete_item():
    query(f"DELETE FROM items WHERE mkt='{request.form.get('mkt')}'")
    return render_template('delete_items.html')



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





#requests
#-------------------------------------------------------------------------------------#

#requests menu
@app.route('/requests_menu')
def requests_menu():
    if session.get('username') != 'admin':
        return redirect('/')
    return render_template('requests_menu.html')



#delete request from db
@app.route('/requests_menu/delete_requests',methods = ['GET','POST'])
def delete_request():
    request_number = request.form.get('request_number')
    query(f"DELETE FROM requests WHERE request_number='{request_number}'")
    return render_template('delete_requests.html')








#export requests table to excel 
@app.route('/download_excel_requests',methods = ['GET','POST'])
def excel_requests():
    with sqlite3.connect('users.db') as conn: 
        query1 = "SELECT * FROM requests" 
        df = pandas.read_sql_query(query1, conn)
    df.to_excel('requests.xlsx',index=False)
    return send_file(
        'requests.xlsx',
        as_attachment=True,
        download_name='requests_data.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

