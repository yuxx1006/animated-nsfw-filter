from pymongo import errors


class ImageFilterStore:

    def __init__(self):
        pass

    # store image filter data into mongodb
    def insert(self, db, image):
        if db is None:
            raise errors.ConnectionFailure
        try:
            rc = db.imagefilter.insert_one(image)
        except errors.DuplicateKeyError as e:
            rc = "DuplicateKeyError: '{}'".format(e)
        return rc

    # get image filter data from mongodb
    def find(self, db, image_id):
        if db is None:
            raise errors.ConnectionFailure
        rc = db.imagefilter.find_one({
            "_id": image_id
        })
        if not rc:
            return "KeyNotFound"
        return rc
