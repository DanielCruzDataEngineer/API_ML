import psycopg2
import pandas as pd
data = pd.read_csv (r'ml_more/ml_more/data.csv',sep=',')   
df = pd.DataFrame(data)
def execute_sql():
    print("Executando query")
    conn = psycopg2.connect(host='35.198.18.5', port='5432',database='postgres',user='postgres', password='postgres')
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS  ml_more (
                price float,
                title char(10000),
                link char(1000)
                );
                delete  from ml_more;
                ''')

    for row in df.itertuples():
        a = row.title.replace("\'",'')
        
        cursor.execute(str('''
                    INSERT INTO ml_more (price, title, link)
                    VALUES ({},'{}','{}')
                    '''
                    ).format(getattr(row, 'price'), a, getattr(row, 'link')))
        
    conn.commit()
execute_sql()		   

