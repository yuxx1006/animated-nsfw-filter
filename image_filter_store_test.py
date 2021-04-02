
from stores.image_filter_store import ImageFilterStore
from stores.database import MongoDatabase
import pprint

# examples
image = {
    "_id": "532b3b39c804a59d1e2e2462dbaf6606",
    "source": "attachment",
    "neutral": "0.964695",
    "drawings": "0.035198",
    "sexy": "0.000075",
    "hentai": "0.000032",
    "porn": "0.000001"
}
image2 = {
    "_id": "1f5a5f34b4a0b280438afd08fa78f70c",
    "source": "emoji",
    "neutral": "0.964695",
    "drawings": "0.035198",
    "sexy": "0.000075",
    "hentai": "0.000032",
    "porn": "0.000001"
}
image3 = {
    "_id": "77700447472717824",
    "source": "emoji",
    "neutral": "0.964695",
    "drawings": "0.035198",
    "sexy": "0.000075",
    "hentai": "0.000032",
    "porn": "0.000001"
}


# ENV = "dev"
#         try:
#             mongodb = MongoDatabase()
#             localhost = mongodb.get_uri(ENV)
#             # localhost = "127.0.0.1:27017" && database_name = troph
#             client = mongodb.connect(localhost)
#             mongo = ImageFilterStore()
#             mongo.insert(client.troph, image)
#         except Exception as e:
#             print(e)

ENV = "local"
try:
    mongodb = MongoDatabase()
    localhost = mongodb.get_uri(ENV)
    #localhost = "localhost:27017"
    client = mongodb.connect(localhost)
    print("client: ", client)

    mongo = ImageFilterStore()
    db = client["troph"]

    results = mongo.insert(db, image2)
    print(results)
    image_id = "1f5a5f34b4a0b280438afd08fa78f70c"
    r2 = mongo.find(db, image_id)
    pprint.pprint(r2)
except Exception as e:
    print(e)
