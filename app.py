#general
#-------------------------------------------------------------------------#  
from flask import Flask,render_template,redirect,request,session,make_response,Response
import pickle,sqlite3,datetime
app = Flask(__name__)
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
    
    for user in users_table:
        if request.form['username'] == user['username']:
            return render_template ("user_error.html")
    query(f"INSERT INTO users VALUES('{request.form['name']}' ,'{request.form['username']}' , '{request.form['password']}' , '{request.form['phone']}' , '{request.form['email']}', '{request.form['team']}' )")
    session['username'] = request.form['username'] 
    return redirect('/')
    
    
     

#items - add items + update items
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
    
    query(f"INSERT INTO items VALUES('{request.form.get('mkt')}', '{request.form.get('category')}', '{request.form.get('item_name')}', '{request.form.get('quantity')}', '{request.form.get('added_by')}','{request.form.get('entrance_date')}','{datetime.datetime.now()}')")
    return render_template('add_items.html')





#update items
@app.route('/items/update', methods = ['GET','POST'])
def update_items():
    if session.get('username') != 'admin':
        return redirect('/')
    
    for item in items_table:
        if request.form.get('mkt') == item['mkt']:
            query(f"UPDATE items SET quantity= quantity +'{int(request.form.get('quantity'))}' WHERE mkt='{request.form.get('mkt')}'")
    query(f"UPDATE items SET added_by='{request.form.get('added_by')}' WHERE mkt='{request.form.get('mkt')}'")
    query(f"UPDATE items SET updating_date='{datetime.datetime.now()}' WHERE mkt='{request.form.get('mkt')}'")
    return render_template('update_items.html')








#show all items
@app.route('/items/items_list')
def items_list():
    if session.get('username') != 'admin':
        return redirect('/')
    
    return render_template('items_list.html',items_table=items_table)






#requests
#----------------------------------------------------------------------------------#

@app.route('/requests',methods = ['POST','GET'])
def requests():
   for user in users_table:
        if session.get('username') == user['username']:
            return render_template('requests.html')
        else:
            return redirect('/login')
        



@app.route('/add_requests',methods = ['POST','GET'])
def add_requests():
   for user in users_table:
        if session.get('username') == user['username']:
            return render_template('add_requests.html')
        else:
            return redirect('/login')





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
    


