<p align="center">
  <img src="venv/static/logo.png" alt="NEXOS Logo" width="80" height="80">
</p>

# NEXOS (Next Release Optimization System) - Backend

Repository for the backend of the graduation project.

###### Developer: Luíza Nurnberg

![Status](https://img.shields.io/badge/Status-Concluded-blue)

## Technologies Used
[![Python](https://skillicons.dev/icons?i=python)](https://www.python.org)
[![Mongo](https://skillicons.dev/icons?i=mongo)](https://www.mongodb.com)
[![Firebase](https://skillicons.dev/icons?i=firebase)](https://firebase.google.com)

## 📘 Mathematical Formulation

The NEXOS system addresses the **Next Release Problem** by identifying the optimal set of software requirements that maximizes customer satisfaction, while respecting the budgetary constraints of the next version.

The mathematical model below (Equations 1 to 5) defines the objective function and constraints that must be satisfied to find an optimal solution.

### 🎯 Objective Function

The goal is to maximize the importance of the satisfied customers weighted by the relevance of each requirement to those customers.

![Objective](https://latex.codecogs.com/svg.image?\color{white}\text{maximize}%20\sum_{i=1}^n%20\sum_{j=1}^m%20X_i%20\cdot%20P_{ij}%20\cdot%20W_j)

Where:
- \(X_i \in \{0, 1\}\): decision variable indicating whether requirement \(i\) is selected
- \(P_{ij}\): importance of requirement \(i\) to customer \(j\)
- \(W_j\): importance of customer \(j\) to the organization

---

### 📏 Constraints

#### 💰 Budget Constraint

The total implementation cost must not exceed the budget \(b\):

![Budget Constraint](https://latex.codecogs.com/svg.image?\color{white}\sum_{i=1}^n%20C_i%20\cdot%20X_i%20\leq%20b)

---

#### 🔗 Requirement Dependency Constraint

If requirement \(X_k\) depends on requirement \(X_l\), then \(X_l\) must be selected when \(X_k\) is:

![Dependency Constraint](https://latex.codecogs.com/svg.image?\color{white}X_k%20\leq%20X_l,%20\quad%20\forall%20(k,l)%20\in%20D)

---

#### 🔘 Binary Decision Variables

Each requirement \(X_i\) and each customer \(Y_j\) is modeled using binary variables:

![X binary](https://latex.codecogs.com/svg.image?\color{white}X_i%20\in%20\{0,1\},%20\quad%201%20\leq%20i%20\leq%20n)

![Y binary](https://latex.codecogs.com/svg.image?\color{white}Y_j%20\in%20\{0,1\},%20\quad%201%20\leq%20j%20\leq%20m)

--- 

## How to Run

- Run `source venv/bin/activate` to activate the virtual environment
- Run `pip freeze > requirements.txt` after installing dependencies
- Navigate to `tcc-nexos-server/venv/src` and run `python3 -B main.py`

### Running Tests

- Run tests from the project root:  
  `PYTHONPATH=venv/src pytest -s tests/`

- Check code coverage:  
  `PYTHONPATH=venv/src pytest --cov=route.kanban.route`

- Remove all `__pycache__` folders:  
  `find . -type d -name "__pycache__" -exec rm -rf {} +`

---