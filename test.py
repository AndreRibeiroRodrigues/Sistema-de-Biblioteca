from pymongo import MongoClient

def get_mongo_connection():
    uri = "mongodb+srv://gamesandre77_db_user:Um.emel2@rayjirmongodb.k4qsfcn.mongodb.net/?appName=RayjirMongodb"
    client = MongoClient(uri)
    db = client["biblioteca"]
    return db

def teste_mongodb():
    db = get_mongo_connection()
    
    # 1. Criar (ou pegar) a coleção
    colecao = db["aluno"]

    # 2. Inserir 1 documento de teste
    documento = {
        "nome": "Teste MongoDB",
        "idade": 22,
        "curso": "ADS"
    }

    resultado = colecao.insert_one(documento)
    print("Documento inserido com o _id:", resultado.inserted_id)

    # 3. Buscar o documento inserido
    encontrado = colecao.find_one({"_id": resultado.inserted_id})
    print("Documento encontrado:", encontrado)

    # 4. Buscar todos
    print("\nTodos os documentos na coleção:")
    for doc in colecao.find():
        print(doc)

if __name__ == "__main__":
    teste_mongodb()