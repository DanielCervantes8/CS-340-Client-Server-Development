# Example Python Code to Insert a Document 


from pymongo import MongoClient
from pymongo.errors import PyMongoError


class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self, username, password): 
        # Initialize the MongoDB connection using the supplied credentials.
        # Connect to the aac database and animals collection.
        # Authentication is performed against the admin database.
        # 
        # Connection Variables 
        # 
        USER = username 
        PASS = password
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient(host=HOST, port=PORT, username=USER, password=PASS, authSource="admin") 
        self.database = self.client[DB] 
        self.collection = self.database[COL] 

    # Create a new animal document in the MongoDB collection.
    
    def create(self, data):
        """Insert a new animal document into MongoDB.

        Args:
            data (dict): Animal information to insert.
                Must be a non-empty dictionary.

        Returns:
            bool: True if MongoDB acknowledges the insertion.
                False if the input is invalid or the operation fails.

        Note:
            MongoDB may add an _id field to the supplied dictionary
            after a successful insertion.
        """
        
        if not isinstance(data, dict) or not data:
            return False
        
        try:
            result = self.collection.insert_one(data)  
            return result.acknowledged
            
        except PyMongoError as error:
            print(f"Create operation failed: {error}")
            return False    

    # Create method to implement the R in CRUD.
    def read(self, query):
        """Retrieve animal documents from MongoDB.

        Args:
            query (dict): MongoDB search criteria.
                An empty dictionary {} retrieves all documents.

        Returns:
            list: Documents matching the query, or an empty list
                if no records match or the operation fails.
        """

        # Verify that the query is a dictionary.
        if not isinstance(query, dict):
            return []

        try:
            # Find all documents matching the query.
            cursor = self.collection.find(query)

            # Convert the MongoDB cursor into a Python list.
            return list(cursor)

        except PyMongoError as error:
            print(f"Read operation failed: {error}")
            return []
        
         # Update animal documents in MongoDB.
    def update(self, query, new_values):
        """Update animal documents matching the MongoDB query.

        Args:
            query (dict): Criteria used to find matching documents.
            new_values (dict): Fields and values to update using $set.

        Returns:
            int: Number of documents actually modified.
                Returns 0 if no documents match, no values change,
                or the operation fails.

        Note:
            A document can match the query without being modified.
            For example, setting a field to its existing value
            does not count as a modification.
        """
        # Verify that the query and new values are dictionaries.
        if not isinstance(query, dict) or not isinstance(new_values, dict):
            return 0

        try:
            # Update all documents that match the query.
            result = self.collection.update_many(
                query,
                {"$set": new_values}
            )

            # Return the number of documents modified.
            return result.modified_count

        except PyMongoError as error:
            print(f"Update operation failed: {error}")
            return 0
        
         # Delete animal documents from MongoDB.
    def delete(self, query):
        """Delete animal documents matching the MongoDB query.

        Args:
            query (dict): Criteria used to identify documents for deletion.

        Returns:
            int: Number of documents successfully deleted.
                Returns 0 if the query is invalid, no documents match,
                or the operation fails.

        Note:
            Empty dictionaries {} are rejected to prevent
            accidental deletion of the entire collection.
            Only non-empty dictionary queries are accepted.
        """

        # Verify that the query is a dictionary.
        if not isinstance(query, dict) or not query:
            return 0

        try:
            # Delete all documents that match the query.
            result = self.collection.delete_many(query)

            # Return the number of documents deleted.
            return result.deleted_count

        except PyMongoError as error:
            print(f"Delete operation failed: {error}")
            return 0