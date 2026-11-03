import asyncio
import logging
from kernel.scheduler import async_stator_consumer_core
from drivers.network import async_payload_producer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("AsyncCoreSync")

async def main():
    wire_queue = asyncio.Queue()
    stop_event = asyncio.Event()
    stats = {"generated": 0, "total_processed": 0, "total_dropped": 0, "master_bank_snapshot": []}

    logger.info("Starting CoreSync Kernel Infrastructure...")
    logger.info("To stream data, send UDP packets via terminal: echo -n 'MyData' > /dev/udp/127.0.0.1/9999")

    # Co-trigger the UDP network listener and the consumer loop engine
    await asyncio.gather(
        async_payload_producer(wire_queue, stop_event, stats),
        async_stator_consumer_core(wire_queue, stop_event, stats)
    )

    print("\n" + "="*75)
    print("LIVE HARMONIC UDP SYSTEM LOG ANALYSIS:")
    print("="*75)
    print(f"Total Network Packets Captured on Wire : {stats['generated']}")
    print(f"Total Packets Processed via Egress Gate: {stats['total_processed']}")
    print(f"Total Dropped Packets (Ring Overrun)  : {stats['total_dropped']}")
    print("-" * 75)
    print("Sample Master Storage Memory Audit Trail:")
    for b in stats["master_bank_snapshot"][:5]:
        print(f"  -> Saved Token: {b.block_id} | Client Source: {b.origin_node:<15} | Payload: {b.payload}")
    print("===========================================================================\n")

if __name__ == "__main__":
    asyncio.run(main())
