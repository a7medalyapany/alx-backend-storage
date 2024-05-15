#!/usr/bin/env python3
'''List all documents in Python'''


def list_all(mongo_collection):
    """
    List all documents in a collection.

    Args:
        mongo_collection: PyMongo collection object.

    Returns:
        A list of documents in the collection.
    """
    all_documents = list(mongo_collection.find({}))
    return all_documents
