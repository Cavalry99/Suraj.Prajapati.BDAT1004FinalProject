import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
creda = credentials.Certificate('key.json')
#firebase_admin.initialize_app(creda, 
#{
#'databaseURL': 'https://suraj-9dad0-default-rtdb.firebaseio.com/'
#})

def update_db():
    db = firestore.client()
    doc_ref = db.collection('car')
    # Import data
    df = pd.read_csv('Canadasalesdata.csv')
    tmp = df.to_dict(orient='records')
    for n, dt in enumerate(tmp):
        dt['id'] = n
        doc_ref.document(str(n)).set(dt)
