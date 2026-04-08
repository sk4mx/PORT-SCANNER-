import socket
import threading
import subprocess
import platform
from datetime import datetime

def ping(host):
    print(f"\n📡 Pinging {host}...\n")
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "4", host]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result.stdout)
    if result.returncode == 0:
        print(f"✅ {host} is reachable!\n")
        return True
    else:
        print(f"❌ {host} is NOT reachable. Exiting.\n")
        return False

def scan_port(host, port, open_ports):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"
            open_ports.append((port, service))
        sock.close()
    except:
        pass

def scan_ports(host, start_port, end_port):
    open_ports = []
    threads = []

    total = end_port - start_port + 1
    print(f"🔍 Scanning {total} ports on {host}...")
    print(f"⏰ Started at: {datetime.now()}\n")

    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(host, port, open_ports))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    open_ports.sort()

    # ── Summary Banner ──────────────────────────
    print("\n" + "=" * 40)
    print(f"   🎯 SCAN RESULTS FOR {host}")
    print("=" * 40)
    print(f"   Total Ports Scanned : {total}")
    print(f"   Open Ports Found    : {len(open_ports)}")
    print(f"   Closed/Filtered     : {total - len(open_ports)}")
    print("=" * 40)

    # ── Open Ports Table ────────────────────────
    if open_ports:
        print(f"\n{'PORT':<10} {'SERVICE':<15} {'STATUS'}")
        print("-" * 35)
        for port, service in open_ports:
            print(f"{port:<10} {service:<15} 🟢 OPEN")

        # ── Quick list ──────────────────────────
        just_ports = [str(p) for p, s in open_ports]
        print(f"\n📋 Open ports list: {', '.join(just_ports)}")
    else:
        print("\n⛔ No open ports found in the given range.")

    print(f"\n⏰ Finished at: {datetime.now()}")

# ─── MAIN ───────────────────────────────────────
domain = input("Enter domain (e.g. example.com): ")

try:
    ip = socket.gethostbyname(domain)
    print(f"\n🌐 Resolved {domain} → {ip}")
except socket.gaierror:
    print("❌ Could not resolve domain. Check the name and try again.")
    exit()

if not ping(ip):
    exit()

start = int(input("Start port: "))
end   = int(input("End port:   "))
scan_ports(ip, start, end)