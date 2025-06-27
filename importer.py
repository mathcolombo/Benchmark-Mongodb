import csv
from datetime import datetime
import random
import time

def parse_datetime_string(dt_str):
    if not dt_str:
        return None
    
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%d",
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(dt_str, fmt)
        except ValueError:
            continue
    print(f"   Aviso: Não foi possível converter data/hora '{dt_str}'. Mantendo como string.")
    return dt_str

def import_csv_data(db_connection, collection_name, file_path):
    collection = db_connection[collection_name]
    collection.delete_many({})

    data_to_insert = []

    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                processed_doc = {}
                for key, value in row.items():
                    if not key:
                        continue

                    try:
                        if value.isdigit():
                            processed_doc[key] = int(value)
                        elif '.' in value and value.replace('.', '', 1).isdigit():
                            processed_doc[key] = float(value)
                        elif value.lower() == 'true':
                            processed_doc[key] = True
                        elif value.lower() == 'false':
                            processed_doc[key] = False
                        else:
                            processed_doc[key] = value.strip()
                    except ValueError:
                        processed_doc[key] = value.strip()

                if collection_name == 'produtos':
                    if 'product_id' in processed_doc and processed_doc['product_id']:
                        processed_doc['_id'] = processed_doc['product_id']
                    
                    for num_field in ["product_name_lenght", "product_description_lenght", "product_photos_qty", "product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"]:
                        if num_field in processed_doc and isinstance(processed_doc[num_field], str):
                            try:
                                processed_doc[num_field] = int(float(processed_doc[num_field]))
                            except ValueError:
                                processed_doc[num_field] = None
                    
                    if 'product_price' not in processed_doc:
                        processed_doc['product_price'] = round(random.uniform(10.0, 1000.0), 2)

                elif collection_name == 'clientes':
                    if 'customer_id' in processed_doc and processed_doc['customer_id']:
                        processed_doc['_id'] = processed_doc['customer_id']
                    
                    if 'customer_city' in processed_doc and isinstance(processed_doc['customer_city'], str):
                         processed_doc['customer_city'] = processed_doc['customer_city'].strip()

                elif collection_name == 'pedidos':
                    if 'order_id' in processed_doc and processed_doc['order_id']:
                        processed_doc['_id'] = processed_doc['order_id']

                    for date_field in ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]:
                        if date_field in processed_doc:
                            processed_doc[date_field] = parse_datetime_string(processed_doc[date_field])
                    
                    if 'customer_id' in processed_doc: 
                        processed_doc['itens'] = [{
                            'product_id': f'DUMMY_PROD_{random.randint(1,10)}', 
                            'product_category_name': 'Eletronicos', 
                            'quantidade': random.randint(1, 3),
                            'preco_unitario': round(random.uniform(50.0, 500.0), 2)
                        }]
                
                data_to_insert.append(processed_doc)
        
        start_time = time.time()

        if data_to_insert:
            collection.insert_many(data_to_insert)
        end_time = time.time()
        print(f"   Importado {len(data_to_insert)} documentos para '{collection_name}' via CSV.")

        return end_time - start_time
    
    except FileNotFoundError:
        print(f"Erro: Arquivo CSV não encontrado em '{file_path}'.")
        return 0
    
    except Exception as e:
        print(f"Erro ao importar CSV '{file_path}': {e}")
        return 0