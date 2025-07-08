from typing import Any
import logging
from modular_robot_task_allocator.core.task.base_task import BaseTask
from modular_robot_task_allocator.utils import raise_with_log

logger = logging.getLogger(__name__)

class Manufacture(BaseTask):
    """ 加工タスクのクラス """
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def update(self) -> bool:
        """
        加工タスクが実行
        完了済み仕事量を 1 増加する
        """
        if not self.is_performance_satisfied() or not self.are_dependencies_completed():
            return False
        if self.assigned_robot is None:
            raise_with_log(RuntimeError, f"Assigned_robot must be initialized: {self.name}.")
        
        self._completed_workload += 1.0
        return True
    