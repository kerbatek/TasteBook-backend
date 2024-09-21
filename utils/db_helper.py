from app import mongo

def select_from_db(collection_name, conditions=None, exclude=None, include_only=None,  one=False):
    if exclude and include_only:
        raise ValueError("Cannot use both exclusions and inclusions in the same query")

    exclusions = {}
    if conditions is None:
        conditions = {}
    if exclude is None:
        exclude = []
    if include_only is None:
        include_only = []
        
    # Prepare the exclusions for the projection
    for key in exclude:
        exclusions[key] = 0
    # Prepare the inclusion for the projection
    for key in include_only:
        exclusions[key] = 1
    
    collection = mongo.db[collection_name]
    
    if one:
        # Return a single document using find_one with exclusions
        return collection.find_one(conditions, exclusions)
    
    # Return multiple documents using find, passing the correct exclusions
    return list(collection.find(conditions, exclusions))


def insert_to_db(collection_name, data):
    collection = mongo.db[collection_name]
    return collection.insert_one(data).inserted_id


def update_db(collection_name, conditions, data):
    collection = mongo.db[collection_name]
    return collection.update_one(conditions, data)