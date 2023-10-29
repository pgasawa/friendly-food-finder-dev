import numpy as np
# from sknetwork.clustering import Louvain
import networkx as nx
# from scipy.sparse import coo_matrix
from sklearn.cluster import SpectralClustering
from friendly_food_finder_dev.firebase import firestore_client

def get_all_users():
    user_docs = firestore_client.get_all_documents_from_collection("users")
    return user_docs

closeness_to_weight = {"Hella tight": 5, "Kinda close": 3, "Lowkey chill": 1}
budget_to_weight = {"$$$$": 4, "$$$": 3, "$$": 2, "$": 1}

class Scheduler:
    def __init__(self, user_email):
        self.user_email = user_email
        self.friends = []
        self.friends_data = {}
        self.friend_emails = []
        self.adjacency_matrix = None
        self.groups = []
        
    def populate_adjacency_matrix(self):
        name_to_idx = {self.friend_emails[i]: i for i in range(len(self.friend_emails))}
        self.adjacency_matrix = [[0 for _ in range(len(self.friend_emails))] for _ in range(len(self.friend_emails))]
        for i in range(len(self.friend_emails)):
            for j in range(len(self.friend_emails)):
                if i == j:
                    continue
                friend_1 = name_to_idx[self.friend_emails[i]]
                friend_2 = name_to_idx[self.friend_emails[j]]
                for friend_obj in self.friends_data[self.friend_emails[i]]:
                    for key in friend_obj:
                        if key == self.friend_emails[j]:
                            self.adjacency_matrix[friend_1][friend_2] = closeness_to_weight[friend_obj[key]["closeness"]]
                for friend_obj in self.friends_data[self.friend_emails[j]]:
                    for key in friend_obj:
                        if key == self.friend_emails[i]:
                            self.adjacency_matrix[friend_2][friend_1] = closeness_to_weight[friend_obj[key]["closeness"]]
                    
        print(self.adjacency_matrix)

    def populate_with_firebase_data(self):
        self.friends = firestore_client.read_from_document("user", self.user_email)["friends"]
        for friend_dict in self.friends:
            for key in friend_dict:
                self.friend_emails.append(key)
        self.friend_emails.append(self.user_email)
        for friend in self.friend_emails:
            self.friends_data[friend] = firestore_client.read_from_document("user", friend)["friends"]
        

    def generate_groupings(self):

        # Create a graph from the adjacency matrix
        n_clusters = max(2, len(self.adjacency_matrix))  # Number of clusters you want to find
        spectral_clustering = SpectralClustering(n_clusters=n_clusters, affinity='precomputed')

        # Fit the model to the adjacency matrix
        labels = spectral_clustering.fit_predict(self.adjacency_matrix)
        self.groups = {i: [] for i in range(0, n_clusters)}
        for i in range(len(labels)):
            self.groups[labels[i]].append(self.friend_emails[i])


    def retrieve_top_groupings(self, k=5):
        return self.groups[:k]