import sys, time
import numpy as np
import pandas as pd

# Transforms the given data into a rating matrix form
# using the pivot_table of the pandas library.
def get_rating_matrix():
    matrix = np.loadtxt(sys.argv[1], dtype='int', usecols=(0, 1, 2))
    matrix = pd.DataFrame({'user': matrix[:, 0],
                           'item': matrix[:, 1],
                           'rating': matrix[:, 2]})
    rating_matrix = matrix.pivot_table('rating', index='user',columns='item', fill_value=0)
    return rating_matrix

# Create a similarity matrix between users
# using Pearson correlation coefficient (PCC) to find neighbors.
def get_similarity_matrix(rating_matrix):
    similarity_matrix = (rating_matrix.T).corr(method='pearson')
    return similarity_matrix

# Estimate the rating of the test data
# By user-based collaborate filtering
def estimate(user, item, rating_matrix, average, neighbors):
    if item not in list(rating_matrix.columns): return average[user]
    weight = weighted_sum = count = 0
    for neighbor in neighbors[user]:
        rate = rating_matrix.loc[neighbor[0]][item]
        if rate == 0: continue
        if(count>len(neighbors[user])/20): break
        weighted_sum += neighbor[1] * (rate - average[user])
        weight += neighbor[1]
        count += 1
    if weight == 0: return average[user]
    prediction = average[user] + weighted_sum / weight
    if prediction > 5: prediction = 5.0
    elif prediction < 1: prediction = 1.0
    return prediction


def predict(rating_matrix, similarity_matrix):
    # Get average rate and neighbors of the each user
    average = dict()
    neighbors = dict()
    for uid in list(rating_matrix.index):
        rating = list(rating_matrix.loc[uid])
        cnt = len(list(filter(lambda x: x!=0, rating)))
        if cnt != 0: average[uid] = sum(rating)/cnt
        else: average[uid] = 0
        neighbor = similarity_matrix[uid].sort_values(ascending=False)
        neighbor = neighbor.reset_index().values.tolist()
        neighbors[uid] = neighbor

    output = sys.argv[1] + "_prediction.txt"
    with open(sys.argv[2], 'r') as test_file, open(output, 'w') as file:
        while True:
            line = test_file.readline().strip()
            if not line or len(line)==0: break
            line = line.split('\t')
            prediction = estimate(int(line[0]), int(line[1]), rating_matrix, average, neighbors)
            result = line[0] + '\t' + line[1] + '\t' + str(prediction) + '\n'
            file.write(result)

if __name__ == "__main__":
    rating_matrix = get_rating_matrix()
    similarity_matrix = get_similarity_matrix(rating_matrix)
    predict(rating_matrix, similarity_matrix)