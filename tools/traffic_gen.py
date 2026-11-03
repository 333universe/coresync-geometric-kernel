import socket
import time
import argparse
import sys

def blast_traffic(port: int, rate_count: int, burst_interval: float):
    """Floods the geometric kernel gateway with high-density UDP frames."""
    target_host = "127.0.0.1"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    print("="*65)
    print(f"🚀 INITIALIZING CORESYNC TRAFFIC BLASTER CORE")
    print("="*65)
    print(f"Target Destination : {target_host}:{port}")
    print(f"Total Target Burst : {rate_count} Datagram packets")
    print(f"Inter-Burst Delay  : {burst_interval} seconds")
    print("-" * 65)
    print("Streaming network frame data. Press Ctrl+C to terminate...")

    start_time = time.time()
    sent_counter = 0

    try:
        for i in range(1, rate_count + 1):
            payload = f"High-Velocity Stress Payload Frame ID #{i:05d}".encode('utf-8')
            sock.sendto(payload, (target_host, port))
            sent_counter += 1
            
            # Apply dynamic pacing delay if specified
            if burst_interval > 0 and i % 10 == 0:
                time.sleep(burst_interval)
                
            if i % 1000 == 0:
                print(f" -> Successfully injected {i} frames into host transport channel...")

    except KeyboardInterrupt:
        print("\n[!] Traffic generation stream interrupted by user.")
    finally:
        duration = time.time() - start_time
        fps = sent_counter / duration if duration > 0 else sent_counter
        print("="*65)
        print("TRAFFIC GENERATION STREAM MATRIX REPORT:")
        print("="*65)
        print(f"Total Packets Pushed to Socket : {sent_counter}")
        print(f"Total Elapsed Burst Duration   : {duration:.4f} seconds")
        print(f"Effective Ingestion Throughput : {fps:.2f} frames/sec")
        print("="*65 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CoreSync Network Performance Traffic Blaster")
    parser.add_argument("-p", "--port", type=int, default=9999, help="Target kernel port")
    parser.add_argument("-c", "--count", type=int, default=5000, help="Number of packets to send")
    parser.add_argument("-d", "--delay", type=float, default=0.0001, help="Delay interval pacing")
    
    args = parser.parse_args()
    blast_traffic(args.port, args.count, args.delay)
