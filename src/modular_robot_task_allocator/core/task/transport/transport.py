import logging
from typing import Any, Union
from numpy.typing import NDArray
import numpy as np
from modular_robot_task_allocator.core.task.base_task import BaseTask
from modular_robot_task_allocator.core.coodinate_utils import is_within_range, make_coodinate_to_tuple
from modular_robot_task_allocator.utils import raise_with_log

logger = logging.getLogger(__name__)

class Transport(BaseTask):
    """ 運搬タスクのクラス """

    def __init__(self, origin_coordinate: Union[tuple[float, float], NDArray[np.float64], list[float]], 
                 destination_coordinate: Union[tuple[float, float], NDArray[np.float64], list[float]],
                 speed: float, **kwargs: Any):
        self._origin_coordinate = make_coodinate_to_tuple(origin_coordinate)  # 出発地点座標
        self._destination_coordinate = make_coodinate_to_tuple(destination_coordinate)  # 目的地座標
        self._speed = speed  # 荷物運搬の難しさ
        super().__init__(**kwargs)

        v = np.array(self.destination_coordinate) - np.array(self.origin_coordinate)
        total = self.transport_resistance * np.linalg.norm(v)
        if self.total_workload != total:
            raise_with_log(ValueError, f"Total_workload does not match carrying_distance * transport_resistance.")
    
    @property
    def origin_coordinate(self) -> tuple[float, float]:
        return self._origin_coordinate
    
    @property
    def destination_coordinate(self) -> tuple[float, float]:
        return self._destination_coordinate
    
    @property
    def speed(self) -> float:
        return self._speed

    def _travel(self, mobility: float) -> None:
        """ 荷物の移動処理 """
        target_coordinate = np.array(self.destination_coordinate)
        v = target_coordinate - np.array(self.coordinate)
        if np.linalg.norm(v) < mobility:
            self.coordinate = self.destination_coordinate
        else:
            self.coordinate = self.coordinate + mobility * v / np.linalg.norm(v)

        if self.assigned_robot is None:
            raise_with_log(RuntimeError, f"Assigned_robot must be initialized.")
        for robot in self.assigned_robot:  # ロボットを荷物に追従
            robot.travel(self.coordinate)
            if not is_within_range(robot.coordinate, self.coordinate):
                raise_with_log(RuntimeError, f"{robot.name} cannot follow the object.")

    def update(self) -> bool:
        """
        運搬タスクが実行
        完了済み仕事量は残り移動距離に応じて計算する
        """
        if not self.is_performance_satisfied() or not self.are_dependencies_completed():
            return False
        if self.assigned_robot is None:
            raise_with_log(RuntimeError, f"Assigned_robot must be initialized: {self.name}.")
            
        mobility_values = [robot.type.performance.get(PerformanceAttributes.MOBILITY, 0) for robot in self.assigned_robot]
        if not mobility_values or max(mobility_values) == 0:
            return False

        min_mobility = min(mobility_values)
        adjusted_mobility = min_mobility / self.transport_resistance
        
        self._travel(adjusted_mobility)

        v = np.array(self.destination_coordinate) - np.array(self.coordinate)
        left = float(np.linalg.norm(v) * self.transport_resistance)
        self._completed_workload = self.total_workload - left
        return True
    