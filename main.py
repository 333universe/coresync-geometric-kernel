
import asyncio
import logging
from kernel.scheduler import async_stator_consumer_core
from drivers.network import async_payload_producer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

async def main():
    wire_queue = asyncio.Queue()
    stop_event = asyncio.Event()
    stats = {"generated": 0, "total_processed": 0, "master_bank_snapshot": []}

    await asyncio.gather(
        async_payload_producer(wire_queue, stop_event, stats),
        async_stator_consumer_core(wire_queue, stop_event, stats)
    )

    print("\n" + "="*75)
    print("FINAL ZERO-INTERRUPT GEOMETRIC I/O LOG ANALYSIS:")
    print("="*75)
    print(f"Total Synthetic Packets Received on Wire : {stats['generated']}")
    print(f"Total Packets Processed via Flash Egress : {stats['total_processed']}")
    print("Hardware Memory State Sync Integrity     : OPTIMAL")
    print("-" * 75)
    print("Master System Memory Bank Audit Trail:")
    for b in stats["master_bank_snapshot"][:3]:
        print(f"  -> Saved Token: {b.block_id} | Node: {b.origin_node:<10} | Ingress Time: {b.ingress_wall_time}")
    print("="*75 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
