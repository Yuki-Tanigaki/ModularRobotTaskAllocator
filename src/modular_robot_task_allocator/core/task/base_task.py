from abc import ABC, abstractmethod
from typing import Any, Union, Optional
from numpy.typing import NDArray
import copy, logging
import numpy as np
from modular_robot_task_allocator.core.robot.robot import Robot, RobotState
from modular_robot_task_allocator.core.coodinate_utils import is_within_range, make_coodinate_to_tuple
from modular_robot_task_allocator.utils import raise_with_log

logger = logging.getLogger(__name__)

class BaseTask(ABC):
    """ タスクを表す抽象基底クラス """

    def __init__(self, name: str, coordinate: Union[tuple[float, float], NDArray[np.float64], list[float]], total_workload: float, 
                 completed_workload: float):
        self._name = name  # タスク名
        self._coordinate = make_coodinate_to_tuple(coordinate)  # タスクの座標
        self._total_workload = total_workload  # タスクの総仕事量
        self._completed_workload = completed_workload  # 完了済み仕事量
        self._task_dependency: Optional[list[BaseTask]] = None  # 依存するタスクのリスト
        self._assigned_robot: list[Robot] = [] # タスクに配置済みのロボットのリスト
        if total_workload < 0.0:
            raise_with_log(ValueError, f"Total_workload must be positive.")
        if completed_workload > total_workload:
            raise_with_log(ValueError, f"Completed_workload exceeds the maximum capacity.")
        if completed_workload < 0.0:
            raise_with_log(ValueError, f"Completed_workload must be positive.")
    
    @property
    def name(self) -> str:
        return self._name

    @property
    def coordinate(self) -> tuple[float, float]:
        return self._coordinate
    
    @coordinate.setter
    def coordinate(self, coordinate: Union[tuple[float, float], NDArray[np.float64], list[float]]) -> None:
        self._coordinate = copy.deepcopy(make_coodinate_to_tuple(coordinate))

    @property
    def total_workload(self) -> float:
        return self._total_workload
    
    @property
    def completed_workload(self) -> float:
        return self._completed_workload
    
    @property
    def task_dependency(self) -> list["BaseTask"]:
        if self._task_dependency is None:
            raise_with_log(RuntimeError, f"Task_dependency must be initialized before use.")
        return self._task_dependency
    
    @property
    def assigned_robot(self) -> list[Robot]:
        return self._assigned_robot

    @abstractmethod
    def update(self) -> bool:
        """ タスクが実行されたときの処理を記述 """
        pass
    
    def initialize_task_dependency(self, task_dependency: list["BaseTask"]) -> None:
        """ タスクの依存関係を設定 """
        self._task_dependency = task_dependency

    def is_completed(self) -> bool:
        """ タスクが完了しているかを確認 """
        return self.completed_workload >= self.total_workload
    
    def are_dependencies_completed(self) -> bool:
        """ 依存するタスクがすべて完了しているかを確認する """
        return all(dep.is_completed() for dep in self.task_dependency)

    def is_performance_satisfied(self) -> bool:
        """ 
        配置されたロボットが必要なパフォーマンスを満たしているか確認
        タスクは複数のロボットの共同作業により実行される
        ロボットの合計能力値が1.0以上の時、タスクは実行される
        """
        total_assigned_performance = 0.0
        for robot in self.assigned_robot:
            for attr, value in robot.type.performance.items():
                if self.__class__.__name__ == attr:
                    total_assigned_performance += value

        return total_assigned_performance >= 1.0

    def release_robot(self) -> None:
        """ 配置されている全ロボットをリリース """
        self._assigned_robot = []

    def assign_robot(self, robot: Robot) -> None:
        """ ロボットを配置 """
        if robot.state != RobotState.ACTIVE:
            raise_with_log(RuntimeError, f"{robot.name} with {robot.state} are assigned.")
        if not is_within_range(robot.coordinate, self.coordinate):
            raise_with_log(RuntimeError, f"{robot.name} with mismatched coordinates are assigned.")

        self._assigned_robot.append(robot)

    def __str__(self) -> str:
        """ タスクを文字列として表示 """
        return f"{self.name}[{self.completed_workload}/{self.total_workload}]"

    def __repr__(self) -> str:
        """ デバッグ用の表現 """
        return f"Task(name={self.name}, completed={self.completed_workload}, total={self.total_workload})"
    
    def __deepcopy__(self, memo: dict[int, Any]) -> "BaseTask":
        raise_with_log(RuntimeError, f"Task class cannot be deepcopied.")