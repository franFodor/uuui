import sys
import numpy as np

class Dataset:
    def __init__(self, data, features) -> None:
        self.data = data
        self.features = features

class NetworkLayer:
    def __init__(self, weights=None, neurons=None, external_weights=None) -> None:
        self.weights = weights
        self.external_weights = external_weights
        self.neurons = neurons

    def __str__(self) -> str:
        return f"\tNeuroni: {self.neurons}\n\tTegovi: {self.weights}\n\tExterni tegovi: {self.external_weights}"

class NeuralNetwork:
    def __init__(self, data, configuration) -> None:
        #print("Ulazim u init...")
        self.configuration = []
        self.layers = []
        self.no_of_layers = 0
        self.error = 0

        for conf in configuration.split("s"):
            if conf:
                self.configuration.append(int(conf))
                self.no_of_layers += 1

        # add input and output layers
        self.no_of_layers += 2 
        #print("konfiguracija:", self.configuration)
        
        # first input amount
        prev_input = len(data.features) - 1
        #print(prev_input)

        for i in range(0, self.no_of_layers):
            layer = NetworkLayer()
            # input layer
            if i == 0:
                layer.weights = np.random.normal(0, 0.01, (self.configuration[i], prev_input))
                layer.external_weights = np.random.normal(0, 0.01, (self.configuration[i], 1))
                layer.neurons = None
                prev_input = self.configuration[i]
            # output layer
            elif i == self.no_of_layers - 1:
                layer.weights = None
                layer.external_weights = None
                layer.neurons = None
            # regular layer
            else:
                # output layer, we only want one external weight
                if i == self.no_of_layers - 2:
                    layer.weights = np.random.normal(0, 0.01, (prev_input, 1))
                    layer.external_weights = np.random.normal(0, 0.01, (1, 1))
                else:
                    layer.weights = np.random.normal(0, 0.01, (self.configuration[i - 1], prev_input))
                    layer.external_weights = np.random.normal(0, 0.01, (self.configuration[i - 1], 1))
                prev_input = self.configuration[i - 1]
                
            # add the generated layer
            self.layers.append(layer)

        print_n = False
                
        if print_n:
            for index, layer in enumerate(self.layers):
                print("Sloj:", index)
                print(layer)
            print("Izlazim iz init....\n")


    def compute(self, data_example) -> None:
        #print("Ulazim u train...")
        input = data_example[:-1]
        # add input to first layer
        self.layers[0].neurons = np.array(input)

        # calculate other layers 
        for index, layer in enumerate(self.layers):
            # skip the first one as there is nothing to calculate for it
            if index == 0:
                continue
            # last one - dont apply sigma gigachad function
            elif index == len(self.layers) - 1:
                #print("Output layer")
                tmp = np.dot(self.layers[index - 1].neurons, self.layers[index - 1].weights)
                parametar = np.add(tmp, self.layers[index - 1].external_weights)
                self.layers[index].neurons = tmp[0] + parametar
                break
            # for every other layer until the last one do the calculation
            else:
                #print("index", index, self.layers[index - 1])
                tmp = np.matmul(self.layers[index - 1].weights, self.layers[index - 1].neurons.transpose())
                parametar = np.add(self.layers[index - 1].external_weights.transpose(), tmp)

                sigmoid = 1 / (1 +np.exp(-parametar))

                self.layers[index].neurons = sigmoid

            print_n = False
                    
            if print_n:
                for index, layer in enumerate(self.layers):
                    print("Sloj:", index)
                    print(layer)
                print("Izlazim iz loopa u train...\n")

        # error

        if len(self.layers[len(self.configuration) + 1].neurons) != 1:
            ValueError("Nevalja neuroni na kraju")
        nn_output_value = self.layers[len(self.configuration) + 1].neurons[0][0]
        real_output_value = data_example[-1]

        error = (real_output_value - nn_output_value) * (real_output_value - nn_output_value)

        self.error = error

        print_n = False
                    
        if print_n:
            for index, layer in enumerate(self.layers):
                print("Sloj:", index)
                print(layer)
            print("Error: ", error)
            print("Izlazim iz train...\n")

    def crossover(self, parent1, parent2) -> None:
        print_n = False

        if print_n:
            print("parent 1")
            for index, layer in enumerate(parent1.layers):
                print("Sloj:", index)
                print(layer)
        if print_n:
            print("parent 2")
            for index, layer in enumerate(parent2.layers):
                print("Sloj:", index)
                print(layer)

        for index, layer in enumerate(parent1.layers):
            if layer.weights is not None:
                tmp = np.add(parent1.layers[index].weights, parent2.layers[index].weights)
                tmp_external = np.add(parent1.layers[index].external_weights, parent2.layers[index].external_weights)
                self.layers[index].weights = tmp * 1/2
                self.layers[index].external_weights = tmp_external * 1/2

        
        if print_n:
            print("child")
            for index, layer in enumerate(self.layers):
                print("Sloj:", index)
                print(layer)
            print("Izlazim iz crossover...\n")

    def mutate(self, mutation_chance, deviation) -> None:
        print_n = False
        
        if print_n:
            for index, layer in enumerate(self.layers):
                print("Sloj:", index)
                print(layer)

        # https://numpy.org/doc/stable/reference/generated/numpy.ndenumerate.html
        for layer in self.layers:
            if layer.weights is not None:
                for index, weight in np.ndenumerate(layer.weights):
                    random_number = np.random.uniform(0, 1)
                    if random_number < mutation_chance:
                        layer.weights[index] += np.random.normal(0, deviation)
                for index, external_weight in np.ndenumerate(layer.external_weights):
                    random_number = np.random.uniform(0, 1)
                    if random_number < mutation_chance:
                        layer.external_weights[index] += np.random.normal(0, deviation)


        if print_n:
            for index, layer in enumerate(self.layers):
                print("Sloj:", index)
                print(layer)

        #exit()
                        

def parse_input(filename) -> Dataset:
    data_input = []
    features = []

    with open(filename) as f:
        header = f.readline()
        header = header.strip()
        header_items = header.split(",")

        for item in header_items:
            features.append(item)

        data = f.readlines()

        for item in data:
            tmp = []
            for znacajka in item.split(","):
                tmp.append(float(znacajka.strip()))
            data_input.append(tmp)

    return Dataset(data_input, features)

def init_population(dataset, popsize, architecture):
    population = []

    for _ in range(0, popsize):
        nn = NeuralNetwork(dataset, architecture)
        population.append(nn) 

    return population

def evaluate(dataset, population):
    for nn in population:
        error = 0
        for data_example in dataset.data:
            nn.compute(data_example)
            error += nn.error
        nn.error = error / len(dataset.data)
        #print(nn.error)
    

# prilagodjeno s: https://stackoverflow.com/questions/10324015/fitness-proportionate-selection-roulette-wheel-selection-in-python
def pick_parents(population):
    #print("Ulazim u pick parent...")
    random_number1 = np.random.random(1)[0]
    random_number2 = np.random.random(1)[0]
    #print("Random numbers:\t", random_number1, random_number2)
    total_error_sum = 0
    parent1_index = -1
    parent2_index = -1

    for resident in population:
        total_error_sum += resident.error

    #print("Total error:\t",total_error_sum)

    fitness_errors = []
    cumsum_errors = np.array([])

    for resident in population:
        fitness_errors.append((1 / resident.error) / (1 / total_error_sum))
    
    # https://numpy.org/doc/stable/reference/generated/numpy.cumsum.html
    cumsum_errors = np.cumsum(fitness_errors)

    #print(cumsum_errors)

    for index, value in enumerate(cumsum_errors):
        if random_number1 < value:
            parent1_index = index
            break
    
    while parent2_index == -1:
        random_number2 = np.random.random(1)[0]
        for index, value in enumerate(cumsum_errors):
            if random_number2 < value and index != parent1_index:
                parent2_index = index
                break

    #print("Indeksi roditelja:", parent1_index, parent2_index)
    return (parent1_index, parent2_index)

def main():
    args = []

    train_file = ""
    test_file = ""
    architecture = ""
    popsize = 0
    elitism = 0
    mutation = 0
    deviation = 0
    iter_count = 0

    for arg in sys.argv:
        args.append(arg)

    args_iter = iter(args)
    for arg in args_iter:
        if arg == "--train":
            train_file = next(args_iter)
        if arg == "--test":
            test_file = next(args_iter)
        if arg == "--nn":
            architecture = next(args_iter)
        if arg == "--popsize":
            popsize = int(next(args_iter))
        if arg == "--elitism":
            elitism = int(next(args_iter))
        if arg == "--p":
            mutation = float(next(args_iter))
        if arg == "--K":
            deviation = float(next(args_iter))
        if arg == "--iter":
            iter_count = int(next(args_iter))

    train_dataset = parse_input(train_file)
    test_dataset = parse_input(test_file)

    #nn = NeuralNetwork(train_dataset, architecture)
    #for data in train_dataset.data:
    #    nn.compute(data)    
    #    break

   # exit()

    population = init_population(train_dataset, popsize, architecture)
    evaluate(train_dataset, population)

    # sort by error
    population = sorted(population, key=lambda x: x.error)

    # genetic algorithm
    for iteration in range(1, iter_count + 1):
    #for iteration in range(1, 3):
        new_population = []
        # elitism
        for i in range(0, elitism):
            #print("Dodajem elitista: ", population[i].error)
            new_population.append(population[i])
        while len(new_population) < popsize:
            parent_indices = pick_parents(population)
            child = NeuralNetwork(train_dataset, architecture)
            child.crossover(population[parent_indices[0]], population[parent_indices[1]])
            #child.crossover(population[0], population[1])
            child.mutate(mutation, deviation)
            new_population.append(child)
            #exit()

        population = new_population
        evaluate(train_dataset, population)

        population = sorted(population, key=lambda x: x.error)
        
        if iteration % 2000 == 0:
            print(f"[Train error {iteration}]: {population[0].error}")

    evaluate(test_dataset, population)
    print(f"[Test error]: {population[0].error}")
    


    return

if __name__ == "__main__":
    main()






