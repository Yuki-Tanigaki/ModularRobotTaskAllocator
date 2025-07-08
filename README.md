# ModularRobotTaskAllocator

## Basic Concepts
A task allocation system for modular robots

## 🚀 Installation

This project uses [Poetry](https://python-poetry.org/) for dependency and environment management.

### 1. Install Poetry (if not already installed)

```bash
pip install poetry
```

### 2. Clone the Repository

```bash
git clone https://github.com/Yuki-Tanigaki/ModularRobotTaskAllocator.git
cd ModularRobotTaskAllocator
```

### 3. Install Dependencies
```bash
poetry install
```

### 4. Activate the Virtual Environment
```bash
poetry shell
```

## How to Use
### Install


### Run Tests
```
poetry run pytest -s
```

### Run mypy
```
poetry run mypy modutask/core/
```

### Run Robot-Configuration
```python
poetry run python optimize_configuration.py --property_file configs/optimize_configuration_sample/property.yaml
```

### Run Task-allocation
```python
poetry run python modutask/task_allocation.py --property_file configs/task_allocation_sample/property.yaml
```


### Run Simulation
```python
poetry run python simulation_launcher.py --property_file configs/simulation_sample/property.yaml
```

