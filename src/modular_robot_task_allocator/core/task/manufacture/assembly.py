import logging
from typing import Any
import numpy as np
from modular_robot_task_allocator.core.module.module import ModuleState
from modular_robot_task_allocator.core.task.base_task import BaseTask
from modular_robot_task_allocator.core.robot.robot import Robot
from modular_robot_task_allocator.core.coodinate_utils import is_within_range

logger = logging.getLogger(__name__)

class Assembly(BaseTask):
    """ ロボット自己組み立てタスク """
    def __init__(self, name: str, robot: Robot):
        missingComponents = robot.missing_components()
        
        total_workload = len(missingComponents)
        super().__init__(name=name, coordinate=robot.coordinate, total_workload=total_workload, 
                         completed_workload=0.0)
        self._target_robot = robot
        self.initialize_task_dependency([])

    @property
    def target_robot(self) -> Robot:
        return self._target_robot

    def update(self) -> bool:
        """ 対象のロボットを組み立てる """
        if self.is_completed():
            return False
        for module in self.target_robot.missing_components():
            if module.state == ModuleState.ERROR:
                continue
            if is_within_range(module.coordinate, self.target_robot.coordinate):
                self.target_robot.mount_module(module)
                self._completed_workload += 1.0
                return True
        return False


        