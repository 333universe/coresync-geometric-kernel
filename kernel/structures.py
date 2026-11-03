
import time
from collections import deque
from dataclasses import dataclass, field, replace
from typing import Tuple

@dataclass(frozen=True)
class RealWorldDataBlock:
    block_id: str
    origin_node: str
    payload: str
    ingress_wall_time: float = field(default_factory=time.time)

@dataclass(frozen=True)
class DriverState:
    # Pin the ring to a strict hardware limitation (e.g., max 1024 slots)
    hardware_stage: deque = field(default_factory=lambda: deque(maxlen=1024))
    master_storage_bank: list = field(default_factory=list)
    buffer_req: bool = False
    buffer_ack: bool = False
    total_processed: int = 0
    total_dropped: int = 0  # Tracks hardware overruns

    def load_to_hardware_ring(self, block: RealWorldDataBlock) -> "DriverState":
        """Loads a block into the hardware staging ring with strict boundary checks."""
        # Create a copy of the queue to maintain functional state immutability
        new_stage = deque(self.hardware_stage, maxlen=self.hardware_stage.maxlen)
        dropped_increment = 0
        
        if len(new_stage) >= (new_stage.maxlen or 1024):
            dropped_increment = 1
            # deque automatically discards the oldest element when full, 
            # but we explicitly track it here for the log analyzer metrics.
            
        new_stage.append(block)
        return replace(
            self, 
            hardware_stage=new_stage,
            total_dropped=self.total_dropped + dropped_increment
        )
