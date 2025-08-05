import random
import numpy as np
import argparse, yaml, pickle, os, logging
from modular_robot_task_allocator.simulator.simulation import Simulator
from modular_robot_task_allocator.core import *
from modular_robot_task_allocator.io import *
from modular_robot_task_allocator.utils import raise_with_log

logger = logging.getLogger(__name__)


def main():
    """シミュレータの実行"""
    parser = argparse.ArgumentParser(description="Run the robotic system simulator.")
    parser.add_argument("--property_file", type=str, help="Path to the property file")
    args = parser.parse_args()

    try:
        with open(args.property_file, 'r') as f:
            prop = yaml.safe_load(f)
    except FileNotFoundError as e:
        raise_with_log(FileNotFoundError, f"File not found: {e}.")

    random.seed(prop['simulation']['seed'])

    tasks = load_tasks(file_path=prop["load"]["task"])
    tasks = load_task_dependency(file_path=prop["load"]['task_dependency'], tasks=tasks)
    module_types = load_module_types(file_path=prop["load"]['module_type'])
    modules = load_modules(file_path=prop["load"]['module'], module_types=module_types)
    robot_types = load_robot_types(file_path=prop["load"]['robot_type'], module_types=module_types)
    robots = load_robots(file_path=prop["load"]['robot'], robot_types=robot_types, modules=modules)
    has_duplicate_module(robots=robots)
    combined_tasks = add_assembly_task(tasks=tasks, robots=robots)
    simulation_map = load_simulation_map(file_path=prop["load"]['map'])
    risk_scenarios = load_risk_scenarios(file_path=prop["load"]['risk_scenario'])
    task_priorities = {}
    for r_name in robots.keys():
        shuffled_array = list(combined_tasks.keys())
        random.shuffle(shuffled_array)
        task_priorities[r_name] = shuffled_array
    # task_priorities = load_task_priorities(file_path=prop["load"]['task_priority'], robots=robots, tasks=combined_tasks)
    permutation_of_tasks(task_priorities=task_priorities, tasks=combined_tasks, robots=robots)

    max_step = prop['simulation']['max_step']
    training_scenarios = prop['simulation']['training_scenarios']
    varidate_scenarios = prop['simulation']['varidate_scenarios']

    total_remaining_workload = []
    variance_remaining_workload = []
    variance_operating_time = []

    for scenario_names in training_scenarios:
        local_modules = clone_module(modules=modules)
        local_robots = clone_robots(robots=robots, modules=local_modules)
        local_tasks = clone_tasks(tasks=combined_tasks, modules=local_modules, robots=local_robots)
        local_scenarios = clone_risk_scenarios(risk_scenarios=risk_scenarios)
        local_map = clone_simulation_map(simulation_map=simulation_map)
        simulator = Simulator(
            tasks=local_tasks, 
            robots=local_robots, 
            task_priorities=task_priorities, 
            scenarios=[local_scenarios[scenario_name] for scenario_name in scenario_names],
            simulation_map=local_map,
            )
        for current_step in range(max_step):
            simulator.run_simulation()
        total_remaining_workload.append(simulator.total_remaining_workload())
        variance_remaining_workload.append(simulator.variance_remaining_workload())
        variance_operating_time.append(simulator.variance_operating_time())
    print(
        float(sum(total_remaining_workload) / len(total_remaining_workload)), 
        float(sum(variance_remaining_workload) / len(variance_remaining_workload)),
        float(sum(variance_operating_time) / len(variance_operating_time))
        )

    # tasks = manager.combined_tasks
    # robots = manager.robots
    # task_priorities=manager.task_priorities
    # scenarios = [manager.risk_scenarios[scenario_name] for scenario_name in varidate_scenarios]
    # simulator = Simulator(
    #     tasks=tasks, 
    #     robots=robots, 
    #     task_priorities=task_priorities, 
    #     scenarios=scenarios,
    #     simulation_map=manager.simulation_map,
    #     )
    
    # for current_step in range(max_step):
    #     simulator.run_simulation()
    #     task_template = prop['results']['task']
    #     task_path = task_template.format(index=current_step)
    #     os.makedirs(os.path.dirname(task_path), exist_ok=True)
    #     with open(task_path, "wb") as f:
    #         pickle.dump(manager.tasks, f)
    # print("Varidate scenario evaluation:")
    # print([simulator.total_remaining_workload(), 
    #         simulator.variance_remaining_workload(),
    #         simulator.variance_operating_time()])


if __name__ == '__main__':
    main()