import asyncio
import logging
import random
import time
from kernel.structures import RealWorldDataBlock

logger = logging.getLogger("AsyncCoreSync")

async def async_payload_producer(wire_queue: asyncio.Queue, stop_event: asyncio.Event, stats: dict):
    """Simulates real-world unpredictable network traffic pouring into ingestion channels."""
    logger.info("[PRODUCER] Ingestion queue pipeline spawned successfully.")
    node_pool = ["Node-Alpha", "Node-Beta", "Node-Gamma"]
    
    while not stop_event.is_set():
        await asyncio.sleep(random.uniform(0.0001, 0.0003))
        if stop_event.is_set():
            break
            
        stats["generated"] += 1
        block = RealWorldDataBlock(
            block_id=f"pkt_0x{stats['generated']:03x}",
            origin_node=random.choice(node_pool),
            payload=f"Telemetry payload chunk signature #{stats['generated']}",
            ingress_wall_time=time.time()
        )
        await wire_queue.put(block)

