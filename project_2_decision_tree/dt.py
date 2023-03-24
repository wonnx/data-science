import sys, math, copy
from collections import defaultdict, Counter

# Algorithm for Decision Tree Induction
# use top-down recursive divide-and-conquer manner
def decision_tree(train_samples, attributes, class_label):

    # If all samples for given node belong to the same class
    # then stop the partitioning process
    class_name = list(attributes)[-1]
    labels = set([s[class_name] for s in train_samples])
    if len(labels) == 1: return list(labels)[0]
    
    # If there are no remaining attributes for further partitioning
    # majority voting is employed for classifying the leaf
    if len(attributes) == 1:
        class_count = dict.fromkeys(sorted(set(class_label)), 0)
        for s in train_samples: class_count[s[class_name]] += 1
        return Counter(class_count).most_common()[0][0]

    # Select the test attribute having the highest information gain
    dic = dict()
    total = len(train_samples)
    for A in list(attributes.keys())[:-1]:
        info_A = 0
        for val in attributes[A]:
            new_samples = [s for s in train_samples if s[A] == val]
            class_count = Counter([s[class_name] for s in new_samples])
            s_total = sum(class_count.values())
            entropy = 0
            for cnt in class_count.values():
                entropy += -(cnt/s_total) * math.log(cnt/s_total, 2)
            info_A += (s_total/total)*entropy
        dic[A] = info_A
    test_attribute = min(dic.keys(), key = lambda k : dic[k])
    
    # Create decision tree recursively
    subtree = dict()
    subtree[test_attribute] = dict()
    for val in attributes[test_attribute]:
        new_samples = [s for s in train_samples if s[test_attribute] == val]
        new_attributes = copy.deepcopy(attributes)
        del new_attributes[test_attribute]
        if len(new_samples) == 0: 
            class_count = dict.fromkeys(sorted(set(class_label)), 0)
            for s in train_samples:
                class_count[s[class_name]] += 1
                subtree[test_attribute][val] = Counter(class_count).most_common()[0][0]
        else: subtree[test_attribute][val] = decision_tree(new_samples, new_attributes, class_label)

    return subtree

# Find the leaf node recursively for the test data set
def classify(dt, sample, attributes):
    node = list(dt.keys())[0]
    next_node = sample[node]
    if isinstance(dt[node][next_node], str): return dt[node][next_node]
    else: return classify(dt[node][next_node], sample, attributes)

if __name__ == "__main__":
    input_file = open(sys.argv[1], 'r')
    result = input_file.readline()
    attributes_name = result.strip().split('\t')
    class_name = attributes_name[-1]
    
    train_samples = list()
    attributes = defaultdict(set)
    class_label = set()

    while(True):
        dic = dict()
        line = input_file.readline().strip()
        if not line: break
        for idx, val in enumerate(line.split('\t')):
            dic[attributes_name[idx]] = val
            attributes[attributes_name[idx]].add(val)
        class_label.add(dic[class_name])
        train_samples.append(dic)
    input_file.close()

    decision_tree = decision_tree(train_samples, attributes, class_label)
    
    test_file = open(sys.argv[2], 'r')
    test_attributes_name = test_file.readline().strip().split('\t')
    test_samples = list()

    while(True):
        dic = dict()
        line = test_file.readline().strip()
        if not line: break
        for idx, val in enumerate(line.split('\t')):
            dic[test_attributes_name[idx]] = val
        test_samples.append(dic)
    test_file.close()

    for sample in test_samples:
        result += '\t'.join(list(sample.values())) + '\t'
        result += classify(decision_tree, sample, list(attributes.keys())[:-1]) + '\n'
    
    result_file = open(sys.argv[3], 'w')
    result_file.write(result)
    result_file.close()