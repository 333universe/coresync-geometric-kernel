import asyncio
import logging
from kernel.scheduler import async_stator_consumer_core
from drivers.network import async_payload_producer

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('AsyncCoreSync')

async def async_stress_injector(queue, stats, stop_event):
    logger = logging.getLogger('AsyncCoreSync')
    logger.info('!!! STARTING HIGH-VELOCITY LOAD STRESS INJECTOR !!!')
    packet_idx = 0
    try:
        while not stop_event.is_set():
            for _ in range(200):
                packet_idx += 1
                from kernel.structures import RealWorldDataBlock
                block = RealWorldDataBlock(
                    block_id=str(packet_idx),
                    origin_node='127.0.0.1:STRESS',
                    payload=f'Stress Invariant Load Signature #{packet_idx:06d}'
                )
                await queue.put(block)
                stats['generated'] += 1
            await asyncio.sleep(0.01)
    except asyncio.CancelledError:
        pass

async def main():
    wire_queue = asyncio.Queue()
    stop_event = asyncio.Event()
    stats = {'generated': 0, 'total_processed': 0, 'total_dropped': 0, 'master_bank_snapshot': []}

    logger.info('Starting CoreSync Kernel Infrastructure...')
    logger.info("To stream data, send UDP packets via terminal: echo -n 'MyData' > /dev/udp/127.0.0.1/9999")

    await asyncio.gather(
        async_payload_producer(wire_queue, stop_event, stats),
        async_stator_consumer_core(wire_queue, stop_event, stats),
        async_stress_injector(wire_queue, stats, stop_event)
    )

    print('\n' + '='*75)
    print('LIVE HARMONIC UDP SYSTEM LOG ANALYSIS:')
    print('='*75)
    print(f"Total Network Packets Captured on Wire : {stats['generated']}")
    print(f"Total Packets Processed via Egress Gate: {stats['total_processed']}")
    print(f"Total Dropped Packets (Ring Overrun)  : {stats['total_dropped']}")
    print('-' * 75)
    print('Sample Master Storage Memory Audit Trail:')
    for b in stats['master_bank_snapshot'][:5]:
        print(f"  -> Saved Token: {b.block_id} | Client Source: {b.origin_node:<15} | Payload: {b.payload}")
    print('===============================================================')

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass