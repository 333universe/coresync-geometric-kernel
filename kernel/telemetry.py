import math
from dataclasses import dataclass

@dataclass(frozen=True)
class StatorTelemetry:
    macro_step: int
    global_pointer: float
    local_pressure: float
    egress_gate_open: bool

class StatorGovernor:
    BLOCK_BOUNDS = {"Block_A": 0.3333, "Block_B": 0.6667, "Block_C": 1.0}
    PHI_GEARS = {"Block_A": 1.0, "Block_B": 1.618033988749895, "Block_C": 2.618033988749895}

    @classmethod
    def analyze_step(cls, macro_step: int) -> StatorTelemetry:
        pointer = round(macro_step * 0.0001, 4)
        if macro_step >= 10000:
            pointer = 1.0

        if pointer <= cls.BLOCK_BOUNDS["Block_A"]:
            block = "Block_A"
        elif pointer <= cls.BLOCK_BOUNDS["Block_B"]:
            block = "Block_B"
        else:
            block = "Block_C"

        # Harmonic Wave: Crosses zero naturally every 0.2500 pointer increments
        # Roots occur at pointer = 0.0, 0.25, 0.5, 0.75, 1.0
        base_wave = math.sin(pointer * math.pi * 4)
        pressure = round(abs(base_wave * cls.PHI_GEARS[block]), 4)

        # The egress gate opens automatically when pressure approaches absolute zero
        egress_gate_open = pressure <= 0.0150

        return StatorTelemetry(
            macro_step=macro_step,
            global_pointer=pointer,
            local_pressure=pressure,
            egress_gate_open=egress_gate_open
        )
