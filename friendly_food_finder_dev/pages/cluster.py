from IPython.display import SVG
import numpy as np
from sknetwork.data import karate_club, painters, movie_actor
from sknetwork.clustering import Louvain, get_modularity
from sknetwork.linalg import normalize
from sknetwork.utils import get_membership
from sknetwork.visualization import svg_graph, svg_bigraph
from scipy.sparse import coo_matrix
from faker import Faker

fake = Faker()

friends = {}

friend_names = [fake.first_name() for _ in range(50)]

for i in range(len(friend_names)):
  my_budget = fake.random_element(elements=("$$$$", "$$$", "$$", "$"))
  friends[friend_names[i]] = {"budget": my_budget, "friends": []}
  for j in range(len(friend_names)):
    if i == j:
      continue
    friend_closeness = fake.random_element(elements=("Hella tight", "Kinda close", "Lowkey chill"))
    budget = fake.random_element(elements=("$$$$", "$$$", "$$", "$"))
    friends[friend_names[i]]["friends"].append({friend_names[j]: {"closeness": friend_closeness, "budget": budget}})

name_to_idx = {friend_names[i]: i for i in range(len(friend_names))}

closeness_to_weight = {"Hella tight": 5, "Kinda close": 3, "Lowkey chill": 1}
budget_to_weight = {"$$$$": 4, "$$$": 3, "$$": 2, "$": 1}

adjacency_matrix = [[0 for _ in range(len(friend_names))] for _ in range(len(friend_names))]

for friend_1 in friends:
  for i in range(len(friends[friend_1]["friends"])):
    for friend_2 in friends[friend_1]["friends"][i]:
      adjacency_matrix[name_to_idx[friend_1]][name_to_idx[friend_2]] = closeness_to_weight[friends[friend_1]["friends"][i][friend_2]["closeness"]]

louvain = Louvain()
adjacency = coo_matrix(adjacency_matrix)
labels = louvain.fit_predict(adjacency)
labels_unique, counts = np.unique(labels, return_counts=True)
position = np.random.randn(200, 2)
image = svg_graph(adjacency, position, labels=labels)


num_groups = max(labels)
groups = {i: [] for i in range(0, num_groups + 1)}
for i in range(len(labels)):
  groups[labels[i]].append(friend_names[i])
