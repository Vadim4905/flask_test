import sqlite3
from flask import *
from werkzeug.exceptions import abort
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

abs_path = os.path.join(os.getcwd(),'')

UPLOAD_FOLDER =  os.path.join(abs_path,'static/images')
basic_user_avatar = 'static/images/basic_user_avatar.jpg'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

app.config['UPLOAD_FOLDER'] = (UPLOAD_FOLDER)

conn = sqlite3.connect("city_data.db",check_same_thread=False)
conn.row_factory = sqlite3.Row
curs = conn.cursor()
username = ''

# curs.execute("DROP TABLE IF EXISTS users")
# curs.execute("DROP TABLE IF EXISTS cities")

curs.execute("""
CREATE TABLE IF NOT EXISTS cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name_ VARCHAR(50), 
    population_ INTEGER, 
    description_ TEXT, 
    year_of_foundation DATE, 
    image_ VARCHAR(255),
    posted_by VARCHAR(50)
)
""")

curs.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    username_ VARCHAR(50), 
    password_ VARCHAR(50), 
    email_ VARCHAR(50), 
    age_ INTEGER,
    is_login INTEGER,
    avatar VARCHAR(255)
)
""")
# curs.execute("INSERT INTO cities (name_, population_, description_, year_of_foundation, image_,posted_by) VALUES ('Одеса', 1020700, 'Жемчужина у моря', 1794, '../static/images/cities/Одеса/1.jpg','vadym')")
# curs.execute("INSERT INTO cities (name_, population_, description_, year_of_foundation, image_,posted_by) VALUES ('Киев', 2950702, 'Столица Украины', 430, '../static/images/cities/Киев/1.jpg','vadym')")
# curs.execute("INSERT INTO cities (name_, population_, description_, year_of_foundation, image_,posted_by) VALUES ('Харьков', 1421125, 'Ну не четак город', 1654, '../static/images/cities/Харьков/1.jpg','vadym')")
# curs.execute("INSERT INTO cities (name_, population_, description_, year_of_foundation, image_,posted_by) VALUES ('Львов', 728545, 'Крутая древняя архитектура', 1256, '../static/images/cities/Львов/1.jpg','vadym')")
# curs.execute("INSERT INTO cities (name_, population_, description_, year_of_foundation, image_,posted_by) VALUES ('Николаев', 470011, 'Один из крупнейших экономических центров юга Украины', 1789, '../static/images/cities/Николаев/1.jpg','vadym')")
# curs.execute("INSERT INTO cities (name_, population_, description_, year_of_foundation, image_,posted_by) VALUES ('Полтава', 279593, 'Важный культурный центр, крупный транспортный узел',    899, '../static/images/cities/Полтава/1.jpg','vadym')")
# curs.execute("INSERT INTO cities (name_, population_, description_, year_of_foundation, image_,posted_by) VALUES ('Мариуполь', 425681, 'Важный культурный центр, крупный транспортный узел',  1778 , '../static/images/cities/Мариуполь/1.jpg','vadym')")
# curs.execute("INSERT INTO cities (name_, population_, description_, year_of_foundation, image_,posted_by) VALUES ('Херсон', 279000, 'Важный экономический, промышленный и культурный центр юга Украины',  1778 , '../static/images/cities/Херсон/1.jpg','vadym')")
# curs.execute("INSERT INTO cities (name_, population_, description_, year_of_foundation, image_,posted_by) VALUES ('Днепр', 984473, 'Один из крупнейших промышленных центров Украины', 1776 , '../static/images/cities/Днепр/1.jpg','vadym')")
# curs.execute("INSERT INTO cities (name_, population_, description_, year_of_foundation, image_,posted_by) VALUES ('Донецк', 913323, 'Пятый город Украины по количеству населения', 1869 , '../static/images/cities/Донецк/1.jpg','vadym')")

conn.commit()
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
def get_curr_avatar():
    if not username:
        return None
    return curs.execute('SELECT avatar FROM users WHERE username_ = ?',[username]).fetchone()['avatar']

def save_files(files,save_path):
    if not os.path.isdir(save_path):
        os.mkdir(save_path)
    amount = len(os.listdir(save_path))
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = str(amount) + '.' + filename.rsplit('.', 1)[1]
            file.save(os.path.join(save_path,filename))
            amount +=1

@app.route("/",methods=['GET','POST'])
def index():
    if request.form:
        name = request.form.get('name')
        population = request.form.get('population')
        description = request.form.get('description')
        year_of_foundation = request.form.get('year_of_foundation')
        data = curs.execute("select * from cities where name_ = (?)", [name]).fetchall()
        if data:
            flash('Такой город уже есть')
            return redirect(url_for('add_city'))

        if len(name) > 50:
            flash('Слишком длиное название города')    
            return redirect(url_for('add_city'))

        if len(description) > 500:
            flash('Описание города не может превышать 500 символов')    
            return redirect(url_for('add_city'))
           
        
        files = request.files.getlist('files[]')

        images_path = os.path.join(abs_path,'static/images/cities',name)
        save_files(files,images_path)

        images = os.listdir(images_path)
        if images:
            image =  images[0]
        else:
            flash('Произошла ошибка при загрузке изображени(я/й)')
            return redirect(url_for('add_city'))
        image_path = os.path.join(f'../static/images/cities/{name}',image)        
        curs.execute("INSERT INTO cities (name_, population_, description_, year_of_foundation, image_,posted_by) VALUES ((?), (?), (?), (?), (?),(?))",[name,population,description,year_of_foundation,image_path,username])
        conn.commit()
    curs.execute("SELECT * FROM cities")
    data = curs.fetchall()
    return render_template('index.html', cities=data,username=username,avatar=get_curr_avatar())

@app.route('/city/<city_name>')
def city(city_name):
    city = curs.execute('SELECT * FROM cities WHERE name_ = ?',(city_name,)).fetchone()
    if city is None:
        abort(404)
    images = []
    path = (f'static/images/cities/{city_name}')
    for name in os.listdir(path):
        images.append(f'../static/images/cities/{city_name}/{name}')
    return render_template('city.html',city=city,username=username,images=images,avatar=get_curr_avatar())

@app.route("/login",methods=['GET','POST'])
def login():
    global username
    if username:
        return redirect('/')
    if request.form:
        user_name = request.form.get('username')
        password = request.form.get('password')
        data = curs.execute("select * from users where username_ = (?) and password_ = (?)", [user_name, password]).fetchall()
        if data:
            username = user_name
            return redirect('/')
        else:
            flash('Неправильный пароль или никнейм')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route("/register",methods=['GET','POST'])
def register():
    global username,image_path
    if username:
        return redirect('/')
    if request.form:
        user_name = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        age = int(request.form.get('age'))
        data = curs.execute("select * from users where username_ = (?) or email_ = (?)", [user_name, email]).fetchall()
        if data or user_name == 'Guest':
            if user_name in  [ u['username_'] for u in data] or user_name == 'Guest':
                flash('Этот никнейм уже занят')
                return redirect(url_for('register'))
            flash('Введенная почта  используется в другом аккаунте')
            return redirect(url_for('register'))

        if not 3 < len(user_name) < 21:
            flash('Никнейм должен быть от 4 символов до 20')
            return redirect(url_for('register'))
        if not 5 < len(password) < 21:
            flash('Пароль должен быть от 6 символов до 20')
            return redirect(url_for('register'))
        #register check
        if email[len(email)-10:] !='@gmail.com':
            flash('Неправильный адрес электронной почты')
            return redirect(url_for('register'))
        if not 5 < len(email.rsplit('@gmail.com',1)[0]) < 31:
            flash('Неправильный адрес электронной почты')
            return redirect(url_for('register'))

        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename  = user_name+'.'+filename.rsplit('.', 1)[1]
            save_path = os.path.join(abs_path,'static/images/users')
            file.save(os.path.join(save_path,filename))
            image_path = os.path.join('../static/images/users',filename)
        else:
            image_path = f'../{basic_user_avatar}'
        curs.execute("INSERT INTO users (username_, password_, email_, age_,avatar) VALUES ((?),(?),(?),(?),(?))",[user_name,password,email,age,image_path])
        conn.commit()
        username = user_name
        return redirect('/')
    return render_template('register.html')

@app.route("/add_city")
def add_city():
    if not  username:
        flash('Вы должны зарегестрироваться чтобы добавить новый город ')
        return redirect(url_for('login'))
    if not username:
        return redirect('/login')
    return render_template('add_city.html',username=username,avatar=get_curr_avatar())

@app.route("/sign_out",methods=['GET','POST'])
def sign_out():
    global username
    if not username:
        return redirect(url_for('index'))
    if request.form:
        if request.form['result'] == 'Да':
            username = ''
        return redirect(url_for('index'))
    return render_template('sign_out.html',username=username,avatar=get_curr_avatar())

@app.route("/users")
def all_users():
    users = curs.execute('SELECT * FROM users').fetchall()
    return render_template('all_users.html',users=users,username=username,avatar=get_curr_avatar())

@app.route('/user/<user_name>')
def user(user_name):
    user = curs.execute('SELECT * FROM users WHERE username_ = ?',(user_name,)).fetchone()
    if user is None:
        abort(404)
    posted_city  = curs.execute('SELECT * FROM cities WHERE posted_by = ?',(user_name,)).fetchall()
    return render_template('user.html',user=user,cities=posted_city,username=username,avatar=get_curr_avatar())

app.run(debug=True)

#library cities
#autor can delete/edit his post
#posted date
#admin possible