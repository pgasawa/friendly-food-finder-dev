import numpy as np
# from sknetwork.clustering import Louvain
import networkx as nx
import community 
# from scipy.sparse import coo_matrix
from friendly_food_finder_dev.firebase import firestore_client

def get_all_users():
    user_docs = firestore_client.get_all_documents_from_collection("users")
    return user_docs

closeness_to_weight = {"Hella tight": 5, "Kinda close": 3, "Lowkey chill": 1}
budget_to_weight = {"$$$$": 4, "$$$": 3, "$$": 2, "$": 1}

class Scheduler:
    def __init__(self, user_email):
        self.user_email = user_email
        self.friends = {}
        self.friend_emails = []
        self.adjacency_matrix = None
        # self.louvain = Louvain()
        self.groups = []
        
    def populate_adjacency_matrix(self):
        name_to_idx = {self.friend_emails[i]: i for i in range(len(self.friend_emails))}
        self.adjacency_matrix = [[0 for _ in range(len(self.friend_names))] for _ in range(len(self.friend_names))]

        for friend_1 in self.friends:
            for i in range(len(self.friends[friend_1]["friends"])):
                for friend_2 in self.friends[friend_1]["friends"][i]:
                    self.adjacency_matrix[name_to_idx[friend_1]][name_to_idx[friend_2]] = closeness_to_weight[self.friends[friend_1]["friends"][i][friend_2]["closeness"]]

    def populate_with_firebase_data(self):
        self.friends = firestore_client.read_from_document("user", self.user_email)["friends"]
        self.friend_emails = [email for email in self.friends]

    def generate_groupings(self):
        # adjacency = coo_matrix(self.adjacency_matrix)
        # labels = self.louvain.fit_predict(adjacency)
        # labels_unique, counts = np.unique(labels, return_counts=True)
        # num_groups = max(labels)
        # self.groups = {i: [] for i in range(0, num_groups + 1)}
        # for i in range(len(labels)):
        #     self.groups[labels[i]].append(self.friend_names[i])

        # Create a graph from the adjacency matrix
        G = nx.Graph()
        for i in range(len(self.adjacency_matrix)):
            for j in range(len(self.adjacency_matrix[i])):
                if self.adjacency_matrix[i][j] > 0:
                    G.add_edge(i, j, weight=self.adjacency_matrix[i][j])

        # Apply the Louvain algorithm for community detection
        partition = community.best_partition(G)
        print(partition)

    def retrieve_top_groupings(self, k=5):
        return self.groups[:k]

scheduler = Scheduler("ayushibatwara@gmail.com")
scheduler.populate_with_firebase_data()
scheduler.populate_adjacency_matrix()
scheduler.generate_groupings()
print(scheduler.groups)