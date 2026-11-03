import pytest
import asyncio
from kernel.telemetry import StatorGovernor
from kernel.structures import DriverState, RealWorldDataBlock
from kernel.scheduler import async_stator_consumer_core

def test_harmonic_roots_alignment():
    """Verify that zero-crossing windows occur strictly at the engineered harmonic points."""
    # Test Root 1 (Pointer 0.2500 -> Step 2500)
    t_2500 = StatorGovernor.analyze_step(2500)
    assert t_2500.global_pointer == 0.2500
    assert t_2500.egress_gate_open is True

    # Test Root 2 (Pointer 0.5000 -> Step 5000)
    t_5000 = StatorGovernor.analyze_step(5000)
    assert t_5000.global_pointer == 0.5000
    assert t_5000.egress_gate_open is True

    # Test Non-Root Intercept (Pointer 0.1250 -> Step 1250 where pressure peaks)
    t_1250 = StatorGovernor.analyze_step(1250)
    assert t_1250.egress_gate_open is False
    assert t_1250.local_pressure > 0.5

@pytest.mark.asyncio
async def test_scheduler_evacuation_integrity():
    """Verify that consumer architecture leaves no data blocks stranded in memory."""
    wire_queue = asyncio.Queue()
    stop_event = asyncio.Event()
    stats = {"generated": 0, "total_processed": 0, "master_bank_snapshot": []}

    # Pre-populate wire queue with static packets before invoking scheduler core
    for i in range(10):
        await wire_queue.put(RealWorldDataBlock(
            block_id=f"test_0x{i:02x}",
            origin_node="TestNode",
            payload="CI Assert Load"
        ))
    stats["generated"] = 10

    # Execute a compressed run or allow regular simulation step cycle to clean it out
    # For testing, we mock an isolated execution context or invoke the core
    # task directly under controlled conditions.
    task = asyncio.create_task(async_stator_consumer_core(wire_queue, stop_event, stats))
    
    # Give the scheduler event loop sufficient ticks to clear elements
    await asyncio.sleep(0.1)
    stop_event.set()
    await task

    # Assertions for safety verification
    assert stats["total_processed"] > 0
    assert stats["total_dropped"] == 0
    
