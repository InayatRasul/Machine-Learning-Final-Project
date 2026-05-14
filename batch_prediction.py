import sqlite3
import pandas as pd
import joblib
import schedule
import time
from datetime import datetime

def run_batch_job():
    print(f"Starting batch job at {datetime.now()}")
    model = joblib.load('model.joblib')
    conn = sqlite3.connect('hospital_data.db')
    
    # Load new patient records
    input_df = pd.read_sql("SELECT * FROM input_data WHERE processed = 0", conn)
    
    if not input_df.empty:
        features = input_df.drop(['id', 'processed'], axis=1)
        predictions = model.predict(features)
        
        input_df['prediction'] = predictions
        input_df['timestamp'] = datetime.now()
        
        # Save results
        input_df[['id', 'prediction', 'timestamp']].to_sql('predictions', conn, if_exists='append', index=False)
        
        # Mark as processed
        ids = tuple(input_df['id'].tolist())
        conn.execute(f"UPDATE input_data SET processed = 1 WHERE id IN {ids if len(ids)>1 else '('+str(ids[0])+')'}")
        conn.commit()
    
    conn.close()

schedule.every(10).minutes.do(run_batch_job)

while True:
    schedule.run_pending()
    time.sleep(1)