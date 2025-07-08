import logging
from typing import Any
from .transport import Transport
from modular_robot_task_allocator.core.module import Module
from modular_robot_task_allocator.utils import raise_with_log

logger = logging.getLogger(__name__)

class TransportModule(Transport):
    """ モジュール運搬タスクのクラス """

    def __init__(self, target_module: Module, **kwargs: Any):
        self._target_module = target_module
        total_workload=total_workload

        super().__init__(**kwargs)
        self.initialize_task_dependency([])
        if self.origin_coordinate != target_module.coordinate:
            raise_with_log(ValueError, f"Origin coordinate does not match the target module's coordinate.")

    @property
    def target_module(self) -> Module:
        return self._target_module

    def update(self) -> bool:
        """
        運搬タスクが実行
        モジュールの位置を変更する
        """
        if super().update():
            self._target_module.coordinate = self.coordinate
            return True
        return False

