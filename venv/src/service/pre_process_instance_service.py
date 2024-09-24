# Data structure refactored to receive from the route
def reset():
    return {
        'n': 0,       # number of requirements
        'm': 0,       # number of customers
        'c': [],      # costs of requirements
        'w': [],      # weights/profits of customers
        'v': [],      # weights of requirements given by customers (can be a n x m matrix or a n vector)
        'P': [],      # set of pairs (i,j) where requirement i is a prerequisite of requirement j
        'Q': [],      # set of pairs (i,k) where requirement i is requested by customer k
        'f': 0,       # multiplication factor to compute b
        'b': 0,       # budget
        'S': []       # set of customers associated with each requirement
    }

def initialize_data(data):
    instance = reset()

    # Requirements and budget
    instance['n'] = data.get('numberOfReq')
    instance['m'] = data.get('numberOfClients')
    instance['c'] = data.get('requirements')
    instance['w'] = data.get('customerWeights')
    instance['Q'] = data.get('customerRequests')  # Pairs (i, k) from route
    instance['P'] = data.get('dependencyMatrix')  # Pairs (i, j) from route
    instance['f'] = data.get('budgetFactor', 0.7)  # Default budget factor
    instance['b'] = sum(instance['c']) * instance['f']

    # Adjust the budget rounding
    if instance['b'] - int(instance['b']) == 0.5:
        instance['b'] += 0.01
    instance['b'] = round(instance['b'])

    # Initialize requirement weights
    instance['v'] = [0] * instance['n']

    # Calculate total weights of requirements requested by customers
    for req, cus in instance['Q']:
        instance['v'][req] += instance['w'][cus]

    # Initialize customer list per requirement
    instance['S'] = [[] for _ in range(instance['n'])]
    for req, cus in instance['Q']:
        instance['S'][req].append(cus)

    return instance

def transformation1(instance):
    novel = True
    while novel:
        novel = False
        for req, cus in instance['Q']:
            for reqi, reqj in instance['P']:
                if req == reqj:
                    if (reqi, cus) not in instance['Q']:
                        instance['Q'].append((reqi, cus))
                        novel = True
    # Rebuild customer list for each requirement
    instance['S'] = [[] for _ in range(instance['n'])]
    for req, cus in instance['Q']:
        instance['S'][req].append(cus)
