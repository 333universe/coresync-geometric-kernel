import asyncio
import logging
from dataclasses import replace
from kernel.structures import DriverState
from kernel.telemetry import StatorGovernor

logger = logging.getLogger("AsyncCoreSync")

async def async_stator_consumer_core(wire_queue: asyncio.Queue, stop_event: asyncio.Event, stats: dict):
    """Processes incoming data blocks using null-point egress handshakes."""
    logger.info("=== INITIALIZING GEOMETRIC ZERO-INTERRUPT NIC DRIVER ===")
    driver_state = DriverState()
    milestones = {1, 2500, 3334, 4999, 5000, 5001, 5002, 6667, 10000}
    
    for step in range(1, 10001):
        while not wire_queue.empty():
            live_block = wire_queue.get_nowait()
            driver_state = driver_state.load_to_hardware_ring(live_block)
            wire_queue.task_done()

        telemetry = StatorGovernor.analyze_step(step)

        if step == 5000:
            driver_state = replace(driver_state, buffer_req=False, buffer_ack=False)
        elif step == 5001:
            if len(driver_state.hardware_stage) > 0:
                driver_state = replace(driver_state, buffer_req=True, buffer_ack=False)
        elif step == 5002:
            if driver_state.buffer_req:
                flushed_blocks = driver_state.hardware_stage
                driver_state = replace(
                    driver_state,
                    hardware_stage=[],
                    master_storage_bank=driver_state.master_storage_bank + flushed_blocks,
                    buffer_req=True,
                    buffer_ack=True,
                    total_processed=driver_state.total_processed + len(flushed_blocks)
                )

        if step in milestones:
            logger.info(
                f"Step: {step:>5} | Ptr: {telemetry.global_pointer:.4f} | "
                f"Wave Pressure: {telemetry.local_pressure:.4f} | "
                f"NIC Ring: {len(driver_state.hardware_stage)} psk | "
                f"REQ: {int(driver_state.buffer_req)} ACK: {int(driver_state.buffer_ack)} | "
                f"Master Bank: {len(driver_state.master_storage_bank)}"
            )
            if step == 5002 and driver_state.buffer_ack:
                logger.info(" [FLASH DUMP EVENT] Hardware ring cleared into master array safely.")

        await asyncio.sleep(0.00001)

    stop_event.set()
    stats["total_processed"] = driver_state.total_processed
    stats["master_bank_snapshot"] = driver_state.master_storage_bank
              
