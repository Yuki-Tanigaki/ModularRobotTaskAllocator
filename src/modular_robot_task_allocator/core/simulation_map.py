import copy
from typing import Any
from modular_robot_task_allocator.core.task import Charge

class SimulationMap:
    """ シミュレーションのマップ """
    def __init__(self, charge_stations: dict[str, Charge]):
        self._charge_stations = charge_stations

    @property
    def charge_stations(self) -> dict[str, Charge]:
        return self._charge_stations
    
    def __str__(self) -> str:
        return f"<Map: {len(self.charge_stations)} stations>"

    def __repr__(self) -> str:
        return (f"Map(charge_stations={self.charge_stations!r})")
    
    def __deepcopy__(self, memo: dict[int, Any]) -> "SimulationMap":
        return SimulationMap(
            copy.deepcopy(self.charge_stations, memo),
        )