import pymongo
import time
import csv
import random
from datetime import datetime

import importer 

# Configuração da conexão do banco
MONGO_HOST = 'mongodb://localhost:27017/'
DB_NAME = 'benchmarkpbd'
client = pymongo.MongoClient(MONGO_HOST)
db = client[DB_NAME]


# Métodos auxiliares
def inserir_clientes_dinamico(num_clientes):
    collection = db.clientes
    collection.delete_many({})

    clientes_para_inserir = []

    for i in range(num_clientes):
        cust_id = f'CUST{i:07d}' 
        city_choice = random.choice(['mogi das cruzes', 'sao paulo', 'rio de janeiro', 'belo horizonte'])
        clientes_para_inserir.append({
            '_id': cust_id,
            'customer_unique_id': f'UNIQUE{i:07d}',
            'customer_zip_code_prefix': str(random.randint(10000, 99999)),
            'customer_city': city_choice,
            'customer_state': random.choice(['SP', 'RJ', 'MG', 'RS'])
        })
    
    start_time = time.time()

    if clientes_para_inserir:
        collection.insert_many(clientes_para_inserir)
    end_time = time.time()
    print(f"   Inseridos {len(clientes_para_inserir)} clientes gerados dinamicamente.")

    return end_time - start_time

def inserir_produtos_dinamico(num_produtos):
    collection = db.produtos
    collection.delete_many({})

    produtos_para_inserir = []

    for i in range(num_produtos):
        prod_id = f'PROD{i:07d}'
        produtos_para_inserir.append({
            '_id': prod_id,
            'product_category_name': random.choice(['eletronicos', 'roupas', 'alimentos', 'livros', 'brinquedos']),
            'product_name_lenght': random.randint(10, 60),
            'product_description_lenght': random.randint(50, 500),
            'product_photos_qty': random.randint(1, 5),
            'product_weight_g': random.randint(100, 5000),
            'product_length_cm': random.randint(10, 100),
            'product_height_cm': random.randint(5, 50),
            'product_width_cm': random.randint(5, 50),
            'product_price': round(random.uniform(10.0, 1000.0), 2)
        })
    
    start_time = time.time()

    if produtos_para_inserir:
        collection.insert_many(produtos_para_inserir)
    end_time = time.time()
    print(f"   Inseridos {len(produtos_para_inserir)} produtos gerados dinamicamente.")

    return end_time - start_time

def inserir_pedidos_dinamico(num_pedidos, num_clientes_ref=100, num_produtos_ref=50):
    collection = db.pedidos
    collection.delete_many({})

    pedidos_para_inserir = []

    clientes_disponiveis = list(db.clientes.find({}, {'_id': 1}).limit(num_clientes_ref))
    produtos_disponiveis = list(db.produtos.find({}, {'_id': 1, 'product_category_name': 1, 'product_price': 1}).limit(num_produtos_ref))

    if not clientes_disponiveis:
        print("Aviso: Nenhuma cliente disponível para criar pedidos dinâmicos. Inserir clientes primeiro.")
        return 0
    if not produtos_disponiveis:
        print("Aviso: Nenhum produto disponível para criar pedidos dinâmicos. Inserir produtos primeiro.")
        return 0

    for i in range(num_pedidos):
        order_id = f'ORDER{i:07d}'
        cliente_aleatorio_id = random.choice(clientes_disponiveis)['_id']
        
        num_itens = random.randint(1, 3)
        itens_pedido = []
        total_pedido = 0.0

        for _ in range(num_itens):
            produto_aleatorio = random.choice(produtos_disponiveis)
            quantidade = random.randint(1, 3)
            preco_unitario = produto_aleatorio.get('product_price', round(random.uniform(10.0, 500.0), 2)) 
            itens_pedido.append({
                'product_id': produto_aleatorio['_id'],
                'product_category_name': produto_aleatorio['product_category_name'],
                'quantidade': quantidade,
                'preco_unitario': preco_unitario
            })
            total_pedido += preco_unitario * quantidade
        
        pedidos_para_inserir.append({
            '_id': order_id,
            'customer_id': cliente_aleatorio_id,
            'order_status': random.choice(['delivered', 'shipped', 'processing']),
            'order_purchase_timestamp': datetime.now(),
            'order_approved_at': datetime.now(),
            'order_delivered_carrier_date': datetime.now(),
            'order_delivered_customer_date': datetime.now(),
            'order_estimated_delivery_date': datetime.now(),
            'itens': itens_pedido,
            'total_pedido': round(total_pedido, 2)
        })
    
    start_time = time.time()

    if pedidos_para_inserir:
        collection.insert_many(pedidos_para_inserir)
    end_time = time.time()
    print(f"   Inseridos {len(pedidos_para_inserir)} pedidos gerados dinamicamente.")

    return end_time - start_time

def consulta_simples():
    start_time = time.time()

    count = db.produtos.count_documents({'product_weight_g': {'$gt': 1000}}) 
    end_time = time.time()
    print(f"   Consulta Simples: Encontrados {count} produtos com peso > 1000g.")

    return end_time - start_time

def consulta_complexa():
    pipeline = [
        {
            '$lookup': {
                'from': 'clientes',
                'localField': 'customer_id',
                'foreignField': '_id',
                'as': 'cliente_info'
            }
        },
        { '$unwind': '$cliente_info' },
        { '$unwind': '$itens' },
        {
            '$project': {
                '_id': 0,
                'order_id': '$_id',
                'customer_id': '$cliente_info._id',
                'customer_city': '$cliente_info.customer_city',
                'product_id': '$itens.product_id',
                'product_category_name': '$itens.product_category_name',
                'quantidade': '$itens.quantidade',
                'preco_unitario_item': '$itens.preco_unitario'
            }
        }
    ]
    
    start_time = time.time()

    results = list(db.pedidos.aggregate(pipeline))
    end_time = time.time()
    print(f"   Consulta Complexa: Agregação retornou {len(results)} documentos.")

    return end_time - start_time

def atualizar_produtos():

    start_time = time.time()

    result = db.produtos.update_many(
        {'product_category_name': 'eletronicos'},
        {'$mul': {'product_price': 1.10}}
    )
    end_time = time.time()
    print(f"   Atualização em Massa: {result.modified_count} produtos atualizados.")

    return end_time - start_time

def deletar_clientes():
    start_time = time.time()

    result = db.clientes.delete_many({'customer_city': 'mogi das cruzes'})
    end_time = time.time()
    print(f"   Exclusão em Massa: {result.deleted_count} clientes excluídos.")
    
    return end_time - start_time

def salvar_resultados_csv(resultados, filename='results_mongodb_benchmark.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Operação', 'Tempo (s)'])
        writer.writerows(resultados)
    print(f"\nResultados do benchmark salvos em '{filename}'.")

# Execução do Benchmark
if __name__ == "__main__":
    print("Iniciando benchmark do MongoDB...")
    resultados = []

    print("Preparando: Limpando coleções existentes...")
    db.clientes.delete_many({})
    db.produtos.delete_many({})
    db.pedidos.delete_many({})
    print("Preparação concluída: Coleções limpas.")
    
    CLIENTES_DATASET_PATH = 'datasets/clientes.csv' 
    PRODUTOS_DATASET_PATH = 'datasets/produtos.csv' 
    PEDIDOS_DATASET_PATH = 'datasets/pedidos.csv'   

    print("\n--- Benchmark: Importação de Dados de Datasets ---")
    
    print(f"Importando clientes de: {CLIENTES_DATASET_PATH}")
    tempo_import_clientes = importer.import_csv_data(db, 'clientes', CLIENTES_DATASET_PATH)
    if tempo_import_clientes > 0:
        resultados.append(['Importação Clientes (Arquivo)', tempo_import_clientes])
    
    print(f"Importando produtos de: {PRODUTOS_DATASET_PATH}")
    tempo_import_produtos = importer.import_csv_data(db, 'produtos', PRODUTOS_DATASET_PATH)
    if tempo_import_produtos > 0:
        resultados.append(['Importação Produtos (Arquivo)', tempo_import_produtos])

    print(f"Importando pedidos de: {PEDIDOS_DATASET_PATH}")
    tempo_import_pedidos = importer.import_csv_data(db, 'pedidos', PEDIDOS_DATASET_PATH)
    if tempo_import_pedidos > 0:
        resultados.append(['Importação Pedidos (Arquivo)', tempo_import_pedidos])
    else:
        print("   Aviso: Importação de pedidos falhou ou não há dados. A Consulta Complexa pode não funcionar.")
    
    NUM_CLIENTES_GEAR = 100000 
    NUM_PRODUTOS_GEAR = 50000  
    NUM_PEDIDOS_GEAR = 200000  
    
    print("\n--- Benchmark: Geração e Inserção Dinâmica de Dados ---")

    print(f"Gerando e inserindo {NUM_CLIENTES_GEAR} clientes...")
    tempo_inserir_clientes = inserir_clientes_dinamico(NUM_CLIENTES_GEAR)
    resultados.append(['Inserção Clientes (Dinâmica)', tempo_inserir_clientes])
    
    print(f"Gerando e inserindo {NUM_PRODUTOS_GEAR} produtos...")
    tempo_inserir_produtos = inserir_produtos_dinamico(NUM_PRODUTOS_GEAR)
    resultados.append(['Inserção Produtos (Dinâmica)', tempo_inserir_produtos])

    print(f"Gerando e inserindo {NUM_PEDIDOS_GEAR} pedidos...")
    tempo_inserir_pedidos = inserir_pedidos_dinamico(NUM_PEDIDOS_GEAR, NUM_CLIENTES_GEAR // 2, NUM_PRODUTOS_GEAR // 2)
    resultados.append(['Inserção Pedidos (Dinâmica)', tempo_inserir_pedidos])

    print("\n--- Benchmark das Operações CRUD ---")
    
    tempo = consulta_simples()
    resultados.append(['Consulta Simples', tempo])
    
    tempo = consulta_complexa()
    resultados.append(['Consulta Complexa', tempo])

    tempo = atualizar_produtos()
    resultados.append(['Atualização em Massa', tempo])
    
    tempo = deletar_clientes()
    resultados.append(['Exclusão em Massa', tempo])

    salvar_resultados_csv(resultados)

    client.close()
    print("Benchmark do MongoDB concluído. Conexão fechada.")