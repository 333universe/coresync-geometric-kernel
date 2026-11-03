import asyncio
import logging
from kernel.structures import RealWorldDataBlock

logger = logging.getLogger("AsyncCoreSync")

class CoreSyncUDPProtocol(asyncio.DatagramProtocol):
    """Low-level asynchronous UDP socket listener for the geometric kernel."""
    def __init__(self, wire_queue: asyncio.Queue, stats: dict):
        self.wire_queue = wire_queue
        self.stats = stats
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        logger.info("[DRIVERS] Zero-Preemption UDP Socket successfully bound to interface.")

    def datagram_received(self, data: bytes, addr: tuple):
        """Asynchronously intercepts raw wire data without interrupting CPU execution threads."""
        self.stats["generated"] += 1
        pkt_id = f"pkt_0x{self.stats['generated']:03x}"
        
        try:
            # Decode raw wire payload
            payload_str = data.decode('utf-8', errors='ignore')
        except Exception:
            payload_str = "[Malformatted Binary Stream Data]"

        # Encapsulate directly into a RealWorldDataBlock
        block = RealWorldDataBlock(
            block_id=pkt_id,
            origin_node=f"{addr[0]}:{addr[1]}",
            payload=payload_str
        )
        
        # Non-blockingly inject into the kernel ingestion queue channel
        self.wire_queue.put_nowait(block)

    def connection_lost(self, exc):
        logger.info("[DRIVERS] UDP Network Socket Interface terminated safely.")


async def async_payload_producer(wire_queue: asyncio.Queue, stop_event: asyncio.Event, stats: dict):
    """Spawns the live UDP socket server to listen for network packets over localhost."""
    loop = asyncio.get_running_loop()
    
    # Bind the socket listener to localhost port 9999
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: CoreSyncUDPProtocol(wire_queue, stats),
        local_addr=('127.0.0.1', 9999)
    )
    
    # Keep the listener alive until the kernel initiates a shutdown
    while not stop_event.is_set():
        await asyncio.sleep(0.1)
        
    transport.close()
