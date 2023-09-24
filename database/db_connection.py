from pymongo import MongoClient

def get_data_from_db():
    client = MongoClient("mongodb+srv://anushaphyrdha:rPCHmI65MKGQaKqn@cluster0.aabdvae.mongodb.net/")
    db = client["mlh_vehicle_centralized_data"]
    collection = db["vehicle_efficiency_raw"]
    return list(collection.find())
