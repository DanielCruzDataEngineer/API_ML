

from flask import Flask, render_template, request, redirect, url_for,session,send_file,jsonify,get_flashed_messages

from flask_sqlalchemy import SQLAlchemy
import os
from scrapy_testes import execute_sql
from valid_auth import valid_login
from autenti_oficial import login_required
import csv
print("Flask")
app = Flask(__name__,template_folder='template',static_folder='static')
print("Flask")
app.secret_key = 'the random string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://daniel:@localhost/mysql'
print("Ok")
db = SQLAlchemy(app)
# @app.route('/speed')
# def speed():
#     st = Speedtest()
#     download_speed = st.download()
#     upload_speed = st.upload()
#     return (f"Download speed: {download_speed} Mbps and Upload speed: {upload_speed} Mb")

@app.route('/')
@login_required
def home():
    return render_template('login.html')

@app.route('/welcome', methods=['GET', 'POST'])
@login_required
def index():
    return render_template("search.html")
@app.route("/search", methods=['GET', 'POST'])
@login_required

def search():

    query = session.get('search', None)
    print(query)

    search_term = request.form['search_term']
    # Armazenar o valor em uma variável
    session['search_term'] = search_term
    # Fazer a pesquisa
    os.environ["VAR1"] = search_term
    count = db.session.execute("""SELECT count(*) from ml_more;""").fetchall()
    count = str(count).replace("[","")
    count = str(count).replace("]","")
    count = str(count).replace(",","")
    def execute_query():
        # Criar a consulta usando o SQLAlchemy

        results = db.session.execute("""SELECT * from ml_more;""").fetchall()
        os.system("sh ml_more.sh")
        execute_sql()
        # Escrever os resultados em um arquivo CSV
        csv_file = 'results.csv'
        with open(csv_file, mode='w',encoding='utf_8_sig') as file:
            writer = csv.writer(file)
            writer.writerow(["price", "title","link","valor_parcelado","desconto"])
            for result in results:
                writer.writerow([result.price, result.title,result.link,result.valor_parcelado,result.desconto])
        # Retornar o arquivo CSV como um arquivo anexo
        return send_file(csv_file,
                    mimetype='text/csv',
                    as_attachment=True,
                    download_name = f"{search_term}.csv"
                    )

        
    
    results = search_term
    return render_template('results.html', results=results,count=count) and execute_query() 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtenha os dados do formulário de login
        username = request.form['username']
        password = request.form['password']

        # Verifique se as credenciais são válidas
        if valid_login(username, password):
            # Armazene o usuário em uma sessão
            session['username'] = username
            return redirect(url_for('index'))
            
        else:
            # Exiba uma mensagem de erro
            error = 'Invalid username/password'
            return render_template('login.html', error=error)
    return render_template('login.html')
        
@app.route('/execute_insert', methods=['GET','POST'])
@login_required
def execute_insert():
    execute_sql()

@app.route('/execute_query', methods=['POST','GET'])
@login_required
def execute_query():
    user_ip = request.remote_addr
    # Criar a consulta usando o SQLAlchemy

    results = db.session.execute("""SELECT * from ml_more;""").fetchall()

    # Escrever os resultados em um arquivo CSV
    csv_file = 'results.csv'
    with open(csv_file, mode='w',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["price", "title","link"])
        for result in results:
             writer.writerow([result.price, result.title,result.link])
    # Retornar o arquivo CSV como um arquivo anexo
    return send_file(csv_file,
                 mimetype='text/csv',
                 as_attachment=True,
                 )

    

    
@app.route('/api_v1', methods=['GET'])
def get_users():
    # Execute a query para obter todos os usuários
    results = db.session.execute("""SELECT * from ml_more;""").fetchall()

    # Converte os resultados para um objeto JSON
    users = [dict(row) for row in results]
    return jsonify(users)
    

if __name__ == '__main__':
    app.run(debug=True)
