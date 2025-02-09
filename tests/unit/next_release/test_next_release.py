import pytest
from service.next_release_service import (
    generate_customer_requirements_dict,
    select_customer,
    can_add,
    can_remove,
    heuristic_construction,
    run_heuristic,
)

@pytest.fixture
def sample_data():
    Q = [(0, 0), (1, 0), (2, 1), (3, 1), (4, 2)]  # Requisitos para cada cliente
    w = [10, 20, 30]  # Pesos dos clientes
    c = [5, 10, 15, 20, 25]  # Custos dos requisitos
    b = 40  # Orçamento disponível
    n = len(c)  # Número de requisitos
    m = len(w)  # Número de clientes
    return Q, w, c, b, n, m

def test_generate_customer_requirements_dict(sample_data):
    # Arrange
    Q, w, _, _, _, _ = sample_data

    # Act
    customer_requirements = generate_customer_requirements_dict(Q, w)

    # Assert
    assert customer_requirements[0]['weight'] == 10
    assert set(customer_requirements[0]['requirements']) == {0, 1}
    assert customer_requirements[2]['weight'] == 30


def test_select_customer(sample_data):
    # Arrange
    Q, w, _, _, _, m = sample_data
    customer_requirements = generate_customer_requirements_dict(Q, w)
    remaining_customers = list(range(m))

    # Act
    selected_customer = select_customer(remaining_customers, customer_requirements, 1.0)

    # Assert
    assert selected_customer in remaining_customers


def test_can_add(sample_data):
    # Arrange
    Q, w, c, b, _, _ = sample_data
    customer_requirements = generate_customer_requirements_dict(Q, w)
    total_cost = 0
    added_requirements = [0] * len(c)

    # Act
    can_add_result, total_cost, added_requirements = can_add(0, total_cost, added_requirements, customer_requirements, c, b)

    # Assert
    assert can_add_result
    assert total_cost == 15


def test_can_remove(sample_data):
    # Arrange
    Q, w, c, _, _, _ = sample_data
    customer_requirements = generate_customer_requirements_dict(Q, w)
    total_cost = 15
    added_requirements = [1, 1, 0, 0, 0]

    # Act
    can_remove_result, total_cost, added_requirements = can_remove(0, total_cost, added_requirements, customer_requirements, c)

    # Assert
    assert can_remove_result
    assert total_cost == 0


def test_heuristic_construction(sample_data):
    # Arrange
    Q, w, c, b, n, m = sample_data
    customer_requirements = generate_customer_requirements_dict(Q, w)
    solution = [0] * m
    added_requirements = [0] * n
    total_cost, selected_customers, obj_value = 0, [], 0

    # Act
    solution, total_cost, selected_customers, added_requirements, obj_value = heuristic_construction(
        customer_requirements, solution, 1.0, added_requirements, total_cost, selected_customers, obj_value, m, c, b)

    # Assert
    assert total_cost <= b
    assert sum(solution) > 0


def test_run_heuristic(sample_data):
    # Arrange
    Q, w, c, b, n, m = sample_data

    # Act
    best_solution, best_selected_customers = run_heuristic(Q, w, c, b, n, m, 0.11, 0.38, 0.5, 0.1)

    # Assert
    assert sum(best_solution) > 0
    assert all(req in range(m) for req in best_selected_customers)