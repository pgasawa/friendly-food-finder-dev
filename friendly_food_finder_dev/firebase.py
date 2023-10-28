import firebase_admin
from firebase_admin import credentials, firestore

class Firebase:
    def __init__(self):
        cred = credentials.Certificate("firebase-key.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def read_from_document(self, collection_name: str, document_name: str):
        doc_ref = self.db.collection(collection_name).document(document_name)
        doc_snapshot = doc_ref.get()
        if doc_snapshot.exists:
            document_data = doc_snapshot.to_dict()
            return document_data
        else:
            # Document does not exist
            return None
            
    def query_by_condition(self, collection_name: str, field_name: str, operator: str, value: str):
        docs = self.db.collection(collection_name).where(field_name, operator, value).stream()
        result = []
        for doc in docs:
            result.append(doc.to_dict())
        return result

    def write_data_to_collection(self, collection_name: str, document_name: str, data):
        # print(collection_name, document_name, data)
        collection_ref = self.db.collection(collection_name)
        doc_ref = collection_ref.document(document_name)
        doc_ref.set(dict(data), merge=True)
        # print(f"Document added: {doc_ref}")

    def update_data_in_collection(self, collection_name: str, document_name: str, data):
        doc_ref = self.db.collection(collection_name).document(document_name)
        doc_ref.update(data)

    def delete_data_from_collection(self, collection_name, document_id):
        try:
            doc_ref = self.db.collection(collection_name).document(document_id)
            doc_ref.delete()
            print(
                f"Document {document_id} successfully deleted from {collection_name} collection."
            )
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_all_documents_from_collection(self, collection_name):
        result = []
        docs = self.db.collection(collection_name).stream()
        for doc in docs:
            result.append(doc.to_dict())
        return result

firestore_client = Firebase()

def get_firestore_client():
    return firestore_client
