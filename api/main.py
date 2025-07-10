import pandas as pd
from fastapi import FastAPI
import os

orders_df = None
current_index = 0

current_file_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_file_path, '..', 'data')

def load_and_prepare_data():
    global orders_df

    print("Loading source data...")    
    orders = pd.read_csv(os.path.join(data_path, 'olist_orders_dataset.csv'))
    order_items = pd.read_csv(os.path.join(data_path, 'olist_order_items_dataset.csv'))

    
    print("Processing and merging data...")
    df = pd.merge(order_items, orders, on='order_id')
    
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    df = df.sort_values(by='order_purchase_timestamp', ascending=True).reset_index(drop=True)
    
    orders_df = df
    print("Data loaded successfully!")
    print(f"Total orders to serve: {len(orders_df)}")


app = FastAPI()

load_and_prepare_data()

@app.get("/health")
def healthcheck():
    return {"message": "ok"}

@app.get("/orders")
def get_new_orders():
    global current_index
    batch_size = 100
    
    if current_index >= len(orders_df):
        print("All orders served. Resetting cursor.")
        current_index = 0
        return {"message": "All orders served. Feed has been reset.", "orders": []}

    end_index = current_index + batch_size
    batch = orders_df.iloc[current_index:end_index]
    current_index = end_index
    
    print(f"Serving {len(batch)} orders. Next index: {current_index}")
    
    batch_dict = batch.where(pd.notnull(batch), None).to_dict('records')
    return {"orders": batch_dict}