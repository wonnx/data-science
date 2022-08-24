import sys
import numpy as np
import pandas as pd

# item-based collaborate filtering
if __name__ == "__main__":
    input = np.loadtxt(sys.argv[1], usecols=(0,1,2), dtype="int")
    matrix = pd.DataFrame(input, columns=["user", "item", "rating"])
    rating_matrix = matrix.pivot_table("rating", index="item", columns="user", fill_value=0)
    pcc = (rating_matrix.T).corr(method="pearson")

    # get similar items
    similar_items = dict()
    for item in rating_matrix.index:
        neighbor = pcc[item].sort_values(ascending=False)
        similar_items[item] = neighbor
    
    # get user average rating
    average = dict()
    for user in rating_matrix.columns:
        count = weight = 0
        for rating in rating_matrix[user]:
            if rating != 0:
                count += 1
                weight += rating
        if count == 0: average[user] = 3
        else: average[user] = weight / count
    
    output = sys.argv[1].split('/')[2] + "_prediction.txt"
    with open(sys.argv[2], 'r') as tf, open(output, 'w') as f:
        while True:
            line = tf.readline().strip()
            if not line or len(line) == 0:
                break
            line = line.split('\t')

            user = int(line[0])
            item = int(line[1])
            prediction = 0
            if item not in list(rating_matrix.index):
                prediction = average[user]
            else:
                count = weight = 0
                neighbors = similar_items[item].index
                for i in neighbors:
                    rating = rating_matrix.loc[i][user]
                    if rating == 0: continue
                    weight += rating
                    count += 1
                    if count == 30: break
                prediction = weight / count
            
            result = line[0] + '\t' + line[1] + '\t' + str(prediction) + '\n'
            f.write(result)