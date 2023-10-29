from IPython.display import SVG
import numpy as np
from sknetwork.data import karate_club, painters, movie_actor
from sknetwork.clustering import Louvain, get_modularity
from sknetwork.linalg import normalize
from sknetwork.utils import get_membership
from sknetwork.visualization import svg_graph, svg_bigraph
from scipy.sparse import coo_matrix
from faker import Faker
from firebase import firestore_client

fake = Faker()

def get_all_users():
    user_docs = firestore_client.get_all_documents_from_collection("users")
    return user_docs

closeness_to_weight = {"Hella tight": 5, "Kinda close": 3, "Lowkey chill": 1}
budget_to_weight = {"$$$$": 4, "$$$": 3, "$$": 2, "$": 1}

class Scheduler:
    def __init__(self, user_email):
        self.user_email = user_email
        self.friends = {}
        self.friend_names = []
        self.adjacency_matrix = None
        self.louvain = Louvain()
        self.groups = []
        
    def populate_adjacency_matrix(self):
        name_to_idx = {self.friend_names[i]: i for i in range(len(self.friend_names))}
        self.adjacency_matrix = [[0 for _ in range(len(self.friend_names))] for _ in range(len(self.friend_names))]

        for friend_1 in self.friends:
            for i in range(len(self.friends[friend_1]["friends"])):
                for friend_2 in self.friends[friend_1]["friends"][i]:
                    self.adjacency_matrix[name_to_idx[friend_1]][name_to_idx[friend_2]] = closeness_to_weight[self.friends[friend_1]["friends"][i][friend_2]["closeness"]]

    def populate_with_firebase_data(self):
        self.friends = firestore_client.read_from_document("user", self.user_email)["friends"]
        for i in range(len(self.friend_names)):
            my_budget = fake.random_element(elements=("$$$$", "$$$", "$$", "$"))
            self.friends[self.friend_names[i]] = {"budget": my_budget, "friends": []}
            for j in range(len(self.friend_names)):
                if i == j:
                    continue
                friend_closeness = fake.random_element(elements=("Hella tight", "Kinda close", "Lowkey chill"))
                budget = fake.random_element(elements=("$$$$", "$$$", "$$", "$"))
                self.friends[self.friend_names[i]]["friends"].append({self.friend_names[j]: {"closeness": friend_closeness, "budget": budget}})

    def generate_groupings(self):
        adjacency = coo_matrix(self.adjacency_matrix)
        labels = self.louvain.fit_predict(adjacency)
        labels_unique, counts = np.unique(labels, return_counts=True)
        num_groups = max(labels)
        self.groups = {i: [] for i in range(0, num_groups + 1)}
        for i in range(len(labels)):
            self.groups[labels[i]].append(self.friend_names[i])

    def retrieve_top_groupings(self, k=5):
        return self.groups[:k]