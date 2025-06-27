# Projeto de Benchmark MongoDB com Python

Este documento contém todas as informações necessárias para entender, configurar e executar um benchmark de operações CRUD (Create, Read, Update, Delete) em um banco de dados MongoDB usando Python. Ele oferece duas formas de popular os dados: importação de arquivos CSV ou geração dinâmica.

## 🚀 Começando

Siga estes passos para configurar e executar o benchmark em sua máquina.
Pré-requisitos

Certifique-se de ter o seguinte instalado em seu sistema:

    Python 3.x: Se não tiver, baixe e instale em https://www.python.org/.

    MongoDB: O servidor MongoDB deve estar em execução. Baixe em https://www.mongodb.com/try/download/community.

    Git: Para clonar o repositório. Baixe em https://git-scm.com/downloads.

### 1. Clonar o Repositório

Primeiro, clone este repositório para sua máquina local:

https://github.com/mathcolombo/Benchmark-Mongodb.git
cd Benchmark-Mongodb

### 2. Verificar os Arquivos de Dados

Os arquivos CSV necessários para a importação de dados já estão incluídos na pasta datasets/ dentro do repositório. Certifique-se de que a estrutura seja a seguinte:

    .
    ├── benchmark.py
    ├── importer.py
    ├── .gitignore
    └── datasets/
        ├── clientes.csv
        ├── produtos.csv
        └── pedidos.csv

## ⚙️ Configuração do Benchmark

### Arquivos

benchmark.py: O script principal que orquestra o benchmark, define as operações CRUD e a lógica de geração de dados dinâmicos.

importer.py: Contém funções auxiliares para a importação de dados a partir de arquivos CSV.

### Conexão com o MongoDB

A conexão com o MongoDB é configurada no benchmark.py. Por padrão, ele se conecta a uma instância local:

    MONGO_HOST = 'mongodb://localhost:27017/'
    DB_NAME = 'benchmarkpbd'

Se o seu MongoDB estiver em outro endereço ou porta, ou se você estiver usando um Atlas Cluster, ajuste MONGO_HOST conforme necessário. O nome do banco de dados benchmarkpbd será criado automaticamente se não existir.

## ▶️ Executando o Benchmark

Com as configurações ajustadas, você pode iniciar o benchmark. Certifique-se de que o MongoDB esteja em execução.

Abra seu terminal, navegue até a pasta raiz do projeto (onde está o benchmark.py) e execute:

    python benchmark.py

O script limpará as coleções existentes (clientes, produtos, pedidos), populará os dados conforme o método escolhido internamente no benchmark.py (importação CSV e/ou geração dinâmica), e, em seguida, executará as operações de benchmark (consulta simples, consulta complexa, atualização em massa, exclusão em massa).

Os resultados dos tempos de execução serão exibidos no console e salvos em um arquivo CSV chamado results_mongodb_benchmark.csv na raiz do projeto.

## 🧹 Limpeza

Para limpar as coleções no MongoDB após o benchmark, você pode simplesmente executar o script novamente, pois ele sempre começa limpando as coleções. Alternativamente, você pode conectar-se ao seu MongoDB e dropar o banco de dados benchmarkpbd.
