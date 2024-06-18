# app.py
#import sys
#sys.path.append("c:/programdata/anaconda3/lib/site-packages/joblib")
import joblib  # 導入 joblib 库
#from joblib import dump, load
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash, request, send_file, render_template
# from models import db, User, TrainingDataset, Model, Score
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from werkzeug.utils import secure_filename
import hashlib
import psycopg2
import dbconn

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:xnNAhTcKS4sWL0ElHAkxeDgn6PlUUNZW@dpg-cphb2locmk4c73edth50-a.singapore-postgres.render.com/final_tnah'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '73b487c79d5f496cd4c1b25e49644425'

# db連結


def get_db_connection():
    conn = psycopg2.connect(
        host=dbconn.host,
        database=dbconn.database,
        user=dbconn.user,
        password=dbconn.password
    )
    return conn


def SplitData(dataName="MatchTimelinesFirst15"):
    # 1. 載入數據
    data_path = f"資料集\完整\{dataName}.csv"
    data = pd.read_csv(data_path)
    # 计算分割的索引位置
    split_index = int(len(data) / 10)

    # 分割数据
    test_data = data[:split_index]  # 1/10的数据
    train_data = data[split_index:]  # 9/10的数据

    # 5. 匯出訓練集和測試集到CSV文件
    train_data_path = f'資料集\訓練\{dataName}_train_data.csv'
    test_data_path = f'資料集\測試\{dataName}_test_data.csv'

    train_data.to_csv(train_data_path, index=False)
    test_data.to_csv(test_data_path, index=False)

    print(f'訓練集已匯出到: {train_data_path}')
    print(f'測試集已匯出到: {test_data_path}')
    data_path = {train_data_path, train_data_path}
    return data_path


# 匯入模型
def UseModel(model_file):
    # model_path = f'E:/大四雲端運算期末作品/模型/{studentName}_model.joblib'
    #model_path = f'D:/MatchTimelinesFirst15_Tree.joblib'
    model = joblib.load(model_file)


    # 2. 載入測試數據
    test_data_path = f'資料集\測試\MatchTimelinesFirst15_test_data.csv'

    test_data = pd.read_csv(test_data_path)
    # 分離特徵和標籤
    features = list(test_data.columns[:14])
    X_test = test_data[features]
    y_test = test_data['status']

    pred = model.predict(X_test)

    # 5. 計算準確率
    accuracy = accuracy_score(y_test, pred)
    formatted_accuracy = "{:.2f}".format(accuracy)
    print(type(formatted_accuracy))
    return formatted_accuracy
# db.init_app(app)
# migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/test_db_connection')
def test_db_connection():
    try:
        # 執行一個簡單的查詢來測試連接
        user = User.query.first()
        if user:
            return f"Connected to the database. First user: {user.Username}"
        else:
            return "Connected to the database, but no users found."
    except Exception as e:
        return str(e)


'''@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 查詢用戶
        user = User.query.filter_by(Username=username).first()
        # 檢查用戶是否存在並且密碼是否正確
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.UserID
            session['username'] = user.Username
            session['user_type'] = user.UserType
            flash('Login successful!', 'success')
            return redirect(url_for('upload'))

        # 用戶不存在或密碼錯誤
        flash('Invalid credentials', 'danger')
    return render_template('login.html')'''


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        userpass = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()  # cursor_factory=psycopg2.extras.RealDictCursor
        SQL = f"SELECT username,password,user_type FROM users WHERE username='{username}' AND password='{userpass}';"

        cursor.execute(SQL)
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        # user = user.query.filter_by(username=username).first()
       
        # if (username == user['username'] and hashpass == user['userpass']):
        if user[0] == username and user[1] == userpass:
            session.permanent = True
            session['username'] = username
            if user[2] == 'Student':
                return redirect(url_for('student'))
            else:
                return redirect(url_for('teacher'))
        else:
            return redirect(url_for('login'))
    else:
        if 'username' in session:
            return redirect(url_for('student'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('user_type', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# @app.route('/register', methods=['GET', 'POST'])
# def register():
    # if request.method == 'POST':
    # password = request.form['password']
    # user_type = request.form['user_type']
    # hashed_password = generate_password_hash(password, method='sha256')
    # new_user = User(Username=username, password=hashed_password, UserType=user_type)
    # db.session.add(new_user)
    # db.session.commit()
    # flash('Registration successful!', 'success')
    # return redirect(url_for('login'))
    # return render_template('register.html')

# 教師端


'''@app.route('/teacher', methods=['GET', 'POST'])
def teacher_dashboard():
    if 'user_type' in session and session['user_type'] == 'Teacher':
        if request.method == 'POST':
            dataset_name = request.form['dataset_name']
            training_data_path = request.form['training_data_path']
            validation_data_path = request.form['validation_data_path']
            # new_dataset = TrainingDataset(
            # DatasetName=dataset_name,
            # TeacherID=session['user_id'],
            # TrainingDataPath=training_data_path,
            # ValidationDataPath=validation_data_path
            # )
            # db.session.add(new_dataset)
            # db.session.commit()
            flash('Dataset uploaded successfully!', 'success')
        datasets = TrainingDataset.query.filter_by(
            TeacherID=session['user_id']).all()
        return render_template('teacher.html', datasets=datasets)
    flash('Unauthorized access!', 'danger')
    return redirect(url_for('login'))'''


app.route('/teacher1', methods=['GET', 'POST'])


def teacher_dashboard():
    SplitData()
    return render_template('teacher.html')


# 學生端
@app.route('/student', methods=['GET', 'POST'])
def student():
   return render_template('student.html')


'''@app.route('/rankings')
def rankings():
    models = Model.query.order_by(Model.Accuracy.desc()).all()
    return render_template('rankings.html', models=models)'''


# @app.route('/')
# def upload_file():
 #   return render_template('uploader.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if 'file' not in request.files:
        return '没有选择文件！'

    file = request.files['file']

    if file.filename == '':
        return '没有选择文件！'

    accuracy = UseModel(
        model_file=file)  # 要更新

    conn = get_db_connection()
    cursor = conn.cursor()
    float_accuracy = float(accuracy)
    tree = 'decision_tree_model'   
    #SQL = f"INSERT INTO models (model_name, model_path, accuracy)VALUES ({tree}, 路徑不用了, {float_accuracy});"
    #cursor.execute(SQL)
    SQL = f"INSERT INTO models (model_name, model_path, accuracy) VALUES (%s, %s, %s);"
    cursor.execute(SQL, (tree, '路徑不用了', float_accuracy))
    conn.commit()    
    cursor.close()
    conn.close()

    return render_template('')  # 排名啥的


    

    


@app.route('/update', methods=['GET', 'POST'])
def update():
    return render_template('upload.html')


'''@app.route('/download')
def download():
    return render_template('download.html')'''


@app.route('/download_file', methods=["GET", "POST"])
def download_file():
    # 指定下載的檔案路徑
    file_path = '資料集\訓練\MatchTimelinesFirst15_train_data.csv'  # 替換成你的檔案路徑
    return send_file(file_path, as_attachment=True)


@app.route('/teacher')
def teacher():
    return render_template('teacher.html')


@app.route('/uploaddataset', methods=["GET", "POST"])
def uploaddataset():
    conn = get_db_connection()
    cursor = conn.cursor()
    file = request.files['file']
    if file:
        # 存儲檔案
        filename = secure_filename(file.filename)
        file.save(filename)
        data = SplitData()  # 要更新
        data_path = {'資料集\訓練\MatchTimelinesFirst15_train_data.csv', '資料集\測試\MatchTimelinesFirst15_train_data.csv'}
        data_path_list = list(data_path)

        # 插入資料庫
        SQL = "INSERT INTO training_datasets (dataset_name, training_data_path, validation_data_path) VALUES (%s, %s, %s)"
        cursor.execute(SQL, (file.filename, data_path_list[0], data_path_list[1]))
        conn.commit()

        return render_template('teacher.html')
    




if __name__ == '__main__':
    app.run()
