import sys
import copy
import itertools

def apriori(transaction, minimum_support):
    # variable to save the result of apriori algorithm
    result = ''

    # converting minimum support percentage to number
    nms = (minimum_support/100) * len(transaction)
    candidates = set()
    frequent_patterns = set()

    # when the length of pattern is 1
    length = 1
    for dt in transaction:
        for item in dt:
            if item not in candidates:
                candidates.add(item)
    candidates = sorted(candidates)
    for itemset in candidates:
        if get_support([itemset], transaction) >= nms:
            frequent_patterns.add(itemset)
    frequent_patterns = sorted(frequent_patterns)

    # when the length of pattern is larger then 1
    while True:
        length += 1
        
        # do self join to get candidates, which length is 'length + 1'
        # return the tuples in the candidates set.
        candidates = self_join(frequent_patterns, length)

        # do prune to reduce the number of candidates
        # return the reducted tuples in the candidates set.
        previous_fp = copy.deepcopy(frequent_patterns)
        candidates = prune(candidates, previous_fp, length)

        # testing - check the support of the new candidates
        frequent_patterns = test_support(candidates, nms, transaction)

        if not frequent_patterns:
            break
        else: # If there is a frequent pattern, apply associative rule
            result += association_rule(frequent_patterns, length, transaction)

    return result

# function to get the support of the candidate pattern
def get_support(itemset, transaction):
    count = 0
    for dt in transaction:
        if set(itemset) == set(itemset) & set(dt):
            count += 1
    return count

def self_join(frequent_patterns, length):
    joined_candidates = list()
    for pattern in frequent_patterns:
        # If the length is 2, there will be patterns of length 1
        # in the frequent patterns set, so the iteration is impossible.
        if length == 2:
            pattern = [pattern]
        for item in pattern:
            if item not in joined_candidates:
                joined_candidates.append(item)
    joined_candidates = set(itertools.combinations(sorted(joined_candidates), length))
    return joined_candidates

def prune(candidates, previous_fp, length):
    pruned_candidates = copy.deepcopy(candidates)
    for itemset in candidates:
        # All subset of candidate itemset should be included
        # in the previous frequent pattern set.
        comb = set(itertools.combinations(sorted(itemset), length-1))

        # If the length is 2, there will be itemsets of length 1
        # the form of the items in comb is like (1,)
        if length == 2:
            for item in comb:
                if not set(item).issubset(previous_fp):
                    pruned_candidates.remove(itemset)
                    break
        # If the length is larger than 2,
        # the form of the items in comb is like (1, 2)
        else:
            for item in comb:
                if not set((item,)).issubset(previous_fp):
                    pruned_candidates.remove(itemset)
                    break
    return pruned_candidates

# function to check the pattern's support 
# whether it is higher than minimum support or not
def test_support(candidates, mns, transaction):
    frequent_patterns = copy.deepcopy(candidates)
    for itemset in candidates:
        if get_support(itemset, transaction) < mns:
            frequent_patterns.remove(itemset)
    return frequent_patterns

def association_rule(frequent_patterns, length, transaction):
    line = ''  # result of the association_rule function
    saved_length = length
    for itemset in frequent_patterns:
        while length > 1:
            comb = set(itertools.combinations(itemset, length-1))
            for item in comb:
                item_set = set(item)
                associative_item_set = set(itemset) - item_set
                support = get_support(itemset, transaction)/len(transaction)*100
                confidence = get_support(itemset, transaction)/get_support(item_set, transaction)*100
                line += str(item_set)+'\t'+str(associative_item_set)+'\t'+str('%.2f' % round(support, 2))+'\t'+str('%.2f' % round(confidence, 2))+'\n'
            length -= 1
        length = saved_length
    return line

if __name__ == '__main__':
    minimnum_support = int(sys.argv[1])
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    transaction = list()
    file_1 = open(input_file, 'r')
    while True:
        line = file_1.readline().strip()
        if not line: break
        transaction.append(sorted(map(int, line.split('\t'))))
    file_1.close()
    result = apriori(transaction, minimnum_support)
    file_2 = open(output_file, "w")
    file_2.write(result)
    file_2.close()