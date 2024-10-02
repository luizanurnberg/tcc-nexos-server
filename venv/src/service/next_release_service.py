# import sys
# import random
# import math
# import time

# budgetFactor = 0.7
# constructionPerc = 0.11
# destructionPerc1 = 0.38
# destructionPerc2 = 0.5

# print("aqui")
# def generate_customer_requirements_dict(Q, w):
#     customer_requirements_dict = {}
#     for req, cus in Q:
#         if cus not in customer_requirements_dict:
#             customer_requirements_dict[cus] = {
#                 'weight': w[cus], 'requirements': []}
#         if req not in customer_requirements_dict[cus]['requirements']:
#             customer_requirements_dict[cus]['requirements'].append(req)
#     return customer_requirements_dict

# def select_customer(remaining_customers, customer_requirements_dict, percent_value, reverse=True):
#     sorted_customers = sorted(
#         remaining_customers, key=lambda x: customer_requirements_dict[x]['weight'], reverse=reverse)
#     amount = max(1, int(percent_value * len(sorted_customers)))
#     sample = random.sample(sorted_customers[:amount], 1)
#     return sample[0]

# def can_add(customer, total_cost, added_requirements, customer_requirements_dict, c, b):
#     additional_cost = 0
#     for req in customer_requirements_dict[customer]['requirements']:
#         if added_requirements[req] == 0:
#             additional_cost += c[req]

#     if total_cost + additional_cost <= b:
#         for req in customer_requirements_dict[customer]['requirements']:
#             added_requirements[req] += 1
#         total_cost += additional_cost
#         return True, total_cost, added_requirements
#     else:
#         return False, total_cost, added_requirements

# def can_remove(customer, total_cost, added_requirements, customer_requirements_dict, c):
#     for req in customer_requirements_dict[customer]['requirements']:
#         if added_requirements[req] == 1:
#             total_cost -= c[req]
#     for req in customer_requirements_dict[customer]['requirements']:
#         added_requirements[req] -= 1
#     return True, total_cost, added_requirements

# def heuristic_construction(customer_requirements_dict, solution, k, added_requirements, total_cost, selected_customers, obj_value, m, c, b):
#     remaining_customers = list(range(m))
#     while remaining_customers:
#         customer = select_customer(
#             remaining_customers, customer_requirements_dict, k)
#         remaining_customers.remove(customer)

#         if customer not in selected_customers:
#             can_add_result, total_cost, added_requirements = can_add(
#                 customer, total_cost, added_requirements, customer_requirements_dict, c, b)

#             if can_add_result:
#                 solution[customer] = 1
#                 obj_value += customer_requirements_dict[customer]['weight']
#                 selected_customers.append(customer)

#     return solution, total_cost, selected_customers, added_requirements, obj_value

# def heuristic_destruction(customer_requirements_dict, solution, j, d, selected_customers, total_cost, obj_value, added_requirements, c):
#     num_customers_remove = min(
#         math.ceil(len(selected_customers) * d), len(selected_customers))

#     for _ in range(num_customers_remove):
#         customer = select_customer(
#             selected_customers, customer_requirements_dict, j, True)
#         selected_customers.remove(customer)
#         can_remove_result, total_cost, added_requirements = can_remove(
#             customer, total_cost, added_requirements, customer_requirements_dict, c)

#         if can_remove_result:
#             solution[customer] = 0
#             obj_value -= customer_requirements_dict[customer]['weight']

#     return solution, total_cost, selected_customers, added_requirements, obj_value

# def run_heuristic(Q, w, c, b, n, m, k, j, d, num_iterations=100):
#     start_time = time.time()

#     customer_requirements_dict = generate_customer_requirements_dict(Q, w)

#     best_solution = [0] * m
#     best_total_cost = 0
#     best_selected_customers = []
#     best_obj_value = 0

#     current_solution = [0] * m
#     current_total_cost, selected_customers, added_requirements, obj_value = 0, [], [0] * n, 0

#     for iteration in range(num_iterations):
#         current_solution, current_total_cost, selected_customers, added_requirements, obj_value = heuristic_destruction(
#             customer_requirements_dict, current_solution, j, d, selected_customers, current_total_cost, obj_value, added_requirements, c)
#         current_solution, current_total_cost, selected_customers, added_requirements, obj_value = heuristic_construction(
#             customer_requirements_dict, current_solution, k, added_requirements, current_total_cost, selected_customers, obj_value, m, c, b)

#         if best_obj_value < obj_value:
#             best_solution = current_solution.copy()
#             best_total_cost = current_total_cost
#             best_selected_customers = selected_customers.copy()
#             best_iteration = f"{iteration + 1}/{num_iterations}"
#             best_obj_value = obj_value

#     elapsed_time = time.time() - start_time
#     return best_solution, best_total_cost, best_selected_customers, best_iteration, best_obj_value, elapsed_time
