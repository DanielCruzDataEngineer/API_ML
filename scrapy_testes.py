import psycopg2
import pandas as pd
import mysql.connector
data = pd.read_csv (r'ml_more/data.csv',sep=',')   
df = pd.DataFrame(data)
def execute_sql():
    print("Executando query")
    conn = mysql.connector.connect(
            host = '192.168.18.8',
            user = 'daniel',
            password ='',
            database = 'mysql'

    )
    cursor = conn.cursor()   
 
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS  ml_more (
                    price float,
                    title varchar(1000),
                    link varchar(1000),
                    valor_parcelado varchar(1000),
                    desconto varchar(200)
                    );
                    
                    ''')
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS  mercado_livre_lake (
                    price float,
                    title varchar(1000),
                    link varchar(1000),
                    valor_parcelado varchar(1000),
                    desconto varchar(200)
                    );
                    
                    ''')
    cursor.execute('''
                    DELETE  FROM ML_MORE
                    
                    
                    ''')

    for row in df.itertuples():
        a = row.title.replace("\'",'')
        b = row.valor_com_parcelas.replace("Antes:",'')
        b = b.replace(" reais",',00')

        cursor.execute(str('''
                    INSERT INTO ml_more (price, title, link,valor_parcelado,desconto)
                    VALUES ({},'{}','{}','{}','{}')
                    '''
                    ).format(getattr(row, 'price'), a, getattr(row, 'link'),b,getattr(row, 'desconto')))
        cursor.execute(str('''
                    INSERT INTO mercado_livre_lake (price, title, link,valor_parcelado,desconto)
                    VALUES ({},'{}','{}','{}','{}')
                    '''
                    ).format(getattr(row, 'price'), a, getattr(row, 'link'),b,getattr(row, 'desconto')))
        
    conn.commit()
execute_sql()		   

