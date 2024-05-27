import math
import sys

class Node:
    def __init__(self, value=None, feature=None, subtrees=None) -> None:
        # yes or no for a Leaf, None for regular Node
        self.value = value
        # dataset restriction on the Node
        self.feature = feature
        # link to subtress steming from the current Node
        self.subtrees = subtrees


class Dataset:
    def __init__(self, data, features, class_label) -> None:
        self.data = data
        self.features = features
        self.class_label = class_label


class ID3:
    def __init__(self) -> None:
        self.model = None


    def fit(self, dataset, max_depth) -> None:
        self.model = id3(dataset.data, dataset.data, dataset.features, dataset.class_label, max_depth)


    def predict(self, dataset) -> None:
        # PREDICTIONS
        predictions = []
        proper_result = []

        for example in dataset.data:
            # remove the class value - we need to predict it
            proper_result.append(example.pop(-1))
            #print(example)
            # now traverse the tree with the current example
            predictions.append(get_prediction(example, self.model, dataset.features))
            #break

        print("[PREDICTIONS]:", end=" ")
        for item in predictions:
            print(item, end=" ")
        print("")

        #print(proper_result)

        # ACCURACY
        # check predictions with proper result
        count_correct = 0
        for index, prediction in enumerate(predictions):
            if prediction == proper_result[index]:
                count_correct += 1

        accuracy = 0
        accuracy = count_correct / len(proper_result)

        print(f"[ACCURACY]: {accuracy:.5f}")

        # CONFUSION_MATRIX
        print("[CONFUSION_MATRIX]:")
        unique_values = []

        # get unique class values
        for value in proper_result:
            if value not in unique_values:
                unique_values.append(value)

        unique_values = sorted(unique_values)

        # init the matrix
        rows = len(unique_values)
        matrix = [[0] * rows for _ in range(rows)]

        # fill it
        for index, val in enumerate(predictions):
            matrix[unique_values.index(proper_result[index])][unique_values.index(predictions[index])] += 1

        # print it
        for row_index, val in enumerate(matrix):
            for col_index, val in enumerate(matrix[row_index]):
                print(matrix[row_index][col_index], end=" ")
            print("")


def get_most_common_value(node):
    # find the most common value of the node
    most_common_value = ""

    for value, subtree in node.subtrees.items():
        if subtree.value < most_common_value or most_common_value == "":
            most_common_value = subtree.value

    return most_common_value


def get_prediction(example, node, features):
    # loop until we get to the leaf
    while node.value is None: 
        if not node.feature:
            return get_most_common_value(node)  
        feature_index = features.index(node.feature)
        feature_value = example[feature_index]
        if feature_value in node.subtrees:
            node = node.subtrees[feature_value]
        else:
            # case where the feature is not found (unseen)
            # find the most common in parent
            return get_most_common_value(node)  

    # return the leaf
    return node.value


def argmax(data, features, feature):
    possible_values = []
    # set it to the class index
    feature_index = len(features) 

    for index, element in enumerate(features):
        if element == feature:
            feature_index = index
            break

    for element in data:
        possible_values.append(element[feature_index])

    # https://stackoverflow.com/questions/23240969/python-count-repeated-elements-in-the-list
    values_dict = {i:possible_values.count(i) for i in possible_values}

    # https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
    return (max(sorted(values_dict), key=values_dict.get))


def entropy(data, features, znacajka=None, vrijednost_features=None, count_znacajki=0):
    entropy = 0
    no_of_features_in_class_label = 0
    possible_values = []

    # set it to the class index
    class_index = len(features)  
    feature_index = len(features) 

    for index, element in enumerate(features):
        if element == znacajka:
            feature_index = index
            break

    for element in data:
        possible_values.append(element[class_index])

    # https://stackoverflow.com/questions/23240969/python-count-repeated-elements-in-the-list
    values_dict = {i:possible_values.count(i) for i in possible_values}

    # https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
    no_of_features_in_class_label = len(values_dict)

    values_list = list(values_dict.keys())

    #print("alo")

    for i in range(0, no_of_features_in_class_label):
        count = 0
        for item in data:
            if not znacajka:
                if item[class_index] == values_list[i]:
                    count += 1
            else:
                if item[class_index] == values_list[i] and item[feature_index] == vrijednost_features:
                    count += 1

        #print(count)
        if count != 0 and not znacajka:
            entropy -= count / len(data) * math.log2(count / len(data))
        elif count != 0 and znacajka:
            entropy -= count / count_znacajki * math.log2(count / count_znacajki)
        else:
            entropy -= 0
            #return entropy

    return entropy


def ig(data, features, znacajka):
    information_gain = 0
    starting_entropy = entropy(data, features)

    #print(starting_entropy)

    no_of_features_in_class_label = 0
    possible_values = []

    feature_index = len(features) # set it to the class index

    for index, element in enumerate(features):
        if element == znacajka:
            feature_index = index
            break

    for element in data:
        possible_values.append(element[feature_index])

    # https://stackoverflow.com/questions/23240969/python-count-repeated-elements-in-the-list
    values_dict = {i:possible_values.count(i) for i in possible_values}
    #print(test_dict)

    # https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
    no_of_features_in_class_label = len(values_dict)

    values_list = list(values_dict.keys())

    for i in range(0, no_of_features_in_class_label):
        tmp = 0 # dx kroz d
        for key in values_dict.keys():
            if key == values_list[i]:
                tmp = values_dict[key] / len(data)
                break
        #print("entropija", entropy(data, znacajka, values_list[i], values_dict[values_list[i]])) 
        #print("nez sta", tmp)

        information_gain -= tmp * entropy(data, features, znacajka, values_list[i], values_dict[values_list[i]])

    information_gain += starting_entropy

    return information_gain


def get_unique_values(data, feature, features):
    unique_values = []

    # get the index for accessing in data
    feature_index = 0
    for index, item in enumerate(features):
        if item == feature:
            feature_index = index
            break
    
    # append all unique values to list
    for item in data:
        if item[feature_index] not in unique_values:
            unique_values.append(item[feature_index])

    return unique_values


def split_dataset(data, feature, value, features):
    reduced_dataset = []
    new_item = []
    # get the index for accessing in dataset
    if not feature:
        return reduced_dataset
    
    feature_index = features.index(feature)

    for item in data:
        if item[feature_index] == value:
            # create a new item excluding the feature at feature_index
            new_item = item[:feature_index] + item[feature_index+1:]
            #print(new_item)
            reduced_dataset.append(new_item)
        #print("")
    return reduced_dataset


def all_same_value(data):
    # check if rest of the examples have only one value of class_label
    all_same = True
    last = ""

    for item in data:
        # set it to class_label value
        tmp = item[-1]
        if last == "":
            last = tmp
            continue
        if tmp != last:
            all_same = False

    return all_same


def id3(data, data_parent, features, class_label, max_depth):
    # check if data is empty - it means that we've reached a combination for which we have no example 
    if len(data) == 0:
        # find the most frequent label of parent node
        #print("aaaaaaaaaaaaa", data_parent)
        v = argmax(data_parent, features, class_label)
        return Node(value=v)

    # find the most frequent label of current node 
    v = argmax(data, features, class_label)
    #print(v, data)

    # if we've used all features (max depth tree) OR the dataset has only one value of y 
    if len(features) == 0 or all_same_value(data) or max_depth == 0:
        return Node(value=v)

    # TODO stavit u funkciju x = argmax_ID myb
    # TODO ne treba mi ig vrijednost u X, vec ime featurea koji ima max ig
    # find most discriminative feature
    x = 0
    max_feature = ""

    # TODO paziti na abecedni sort
    for val in features:
        # calculate IG for every feature
        tmp = ig(data, features, val)
        print(f"IG({val}): {tmp:.4f}", end=" ")
        if (tmp > x and max_feature < val):
            max_feature = val
            x = tmp
        elif (tmp == x and max_feature > val):
            max_feature = val
            x = tmp

    print("")

    subtrees = {}
    features_reduced = []

    for item in features:
        if item != max_feature:
            features_reduced.append(item)

    #print("uniq values", get_unique_values(data, max_feature, features), features, features_reduced)
    #print("max", max_feature)

    for value in get_unique_values(data, max_feature, features):
        # get examples which only contain the max feature with current value
        dataset_reduced = split_dataset(data, max_feature, value, features) 
        #print(dataset_reduced)
        subtree = id3(dataset_reduced, data, features_reduced, class_label, max_depth - 1)
        subtrees[value] = subtree
    
    return Node(feature=max_feature, subtrees=subtrees)


def parse_input(filename) -> Dataset:
    data_input = []
    features = []
    class_label = []

    with open(filename) as f:
        header = f.readline()
        header = header.strip()
        header_items = header.split(",")

        for index, item in enumerate(header_items):
            if index == len(header_items) - 1:
                class_label.append(item)
                #features.append(item)
            else:
                features.append(item)

        data = f.readlines()

        for item in data:
            tmp = []
            for znacajka in item.split(","):
                tmp.append(znacajka.strip())
            data_input.append(tmp)

    return Dataset(data_input, features, class_label)


def print_tree(node, branch=[], depth=0):
    if depth == 0:
        print("[BRANCHES]:")
    if node.value is not None:
        print(" ".join(branch + [node.value]))
    else:
        for value, subtree in sorted(node.subtrees.items(), key=lambda x: x[0]):
            print_tree(subtree, branch + [f"{depth + 1}:{node.feature}={value}"], depth + 1)


def main():
    args = []

    for arg in sys.argv:
        args.append(arg)

    max_depth = -1
    train_filename = args[1]
    test_filename = args[2]
    if len(args) > 3:
        max_depth = int(args[3])
    
    train_dataset = parse_input(train_filename)
    test_dataset = parse_input(test_filename)

    model = ID3()
    model.fit(train_dataset, max_depth)
    print_tree(model.model)

    model.predict(test_dataset) 


if __name__ == "__main__":
    main()