import pytest
from kernel.telemetry import StatorGovernor

def test_stator_null_points():
    """Assert pressure properties are forced to zero or deterministic values at boundary nodes."""
    t_5000 = StatorGovernor.analyze_step(5000)
    assert t_5000.local_pressure == 0.0
    assert t_5000.egress_gate_open is True

    t_10000 = StatorGovernor.analyze_step(10000)
    assert t_10000.local_pressure == 0.0
    assert t_10000.global_pointer == 1.0
  
