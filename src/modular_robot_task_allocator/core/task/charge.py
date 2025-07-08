from typing import Any, Union
from numpy.typing import NDArray
import logging, copy
import numpy as np
from modular_robot_task_allocator.core.task.base_task import BaseTask
from modular_robot_task_allocator.utils import raise_with_log

logger = logging.getLogger(__name__)

class Charge(BaseTask):
    """ 充電タスク """
    def __init__(self, charging_speed: float, **kwargs: Any):
        super().__init__(**kwargs)
        self._charging_speed = charging_speed
        self.initialize_task_dependency([])

    @property
    def charging_speed(self) -> float:
        return self._charging_speed

    def update(self) -> bool:
        """ 割り当てられたロボットを充電 """
        if self.assigned_robot is None:
            raise_with_log(RuntimeError, f"Assigned_robot must be initialized.")
        for robot in self.assigned_robot:
            robot.charge_battery_power(self.charging_speed)
        return True
    
    def __deepcopy__(self, memo: dict[int, Any]) -> "Charge":
        clone = Charge(
            copy.deepcopy(self.name, memo),
            copy.deepcopy(self.coordinate, memo),
            copy.deepcopy(self.charging_speed, memo),
        )
        clone._task_dependency = copy.deepcopy(self.task_dependency, memo)
        return clone