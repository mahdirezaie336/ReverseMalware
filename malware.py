from socket import socket
import platform
import psutil
import time
import locale
import json


def get_system_info():
    info = {}
    platform_info = {
        'hostname': platform.node(),
        'os': platform.system(),
        'os_release': platform.release(),
        'os_version': platform.version(),
        'machine': platform.machine(),
        'os_build_type': platform.architecture()[0],
        'system_boot_time': psutil.boot_time(),
        'system_manufacturer': platform.system(),
        'processor': platform.processor(),
    }
    info['platform'] = platform_info

    cpu_info = {
        'cpu_percent': psutil.cpu_percent(),
        'cpu_count': psutil.cpu_count(),
        'cpu_freq': psutil.cpu_freq(),
        'cpu_times': psutil.cpu_times(),
    }
    info['cpu'] = cpu_info

    memory_info = {
        'total': psutil.virtual_memory().total,
        'available': psutil.virtual_memory().available,
        'used': psutil.virtual_memory().used,
        'free': psutil.virtual_memory().free,
        'active': psutil.virtual_memory().active,
        'inactive': psutil.virtual_memory().inactive,
        'buffers': psutil.virtual_memory().buffers,
        'cached': psutil.virtual_memory().cached,
        'shared': psutil.virtual_memory().shared,
        'slab': psutil.virtual_memory().slab,
    }
    info['memory'] = memory_info

    disk_info = {
        'total': psutil.disk_usage('/').total,
        'used': psutil.disk_usage('/').used,
        'free': psutil.disk_usage('/').free,
        'percent': psutil.disk_usage('/').percent,
    }
    info['disk'] = disk_info

    network_info = {
        'bytes_sent': psutil.net_io_counters().bytes_sent,
        'bytes_recv': psutil.net_io_counters().bytes_recv,
        'packets_sent': psutil.net_io_counters().packets_sent,
        'packets_recv': psutil.net_io_counters().packets_recv,
        'errin': psutil.net_io_counters().errin,
        'errout': psutil.net_io_counters().errout,
        'dropin': psutil.net_io_counters().dropin,
        'dropout': psutil.net_io_counters().dropout,
    }
    info['network'] = network_info

    locale_info = {
        'preferred_encoding': locale.getpreferredencoding(),
        'timezones': time.tzname,
    }
    info['locale'] = locale_info

    return json.dumps(info)


def start_client(host, port):
    # Create socket
    client = socket()
    client.connect((host, port))
    print(f"Connected to {host}:{port}")

    # Receive command from server
    try:
        while True:
            command = client.recv(1024).decode()
            print(f"Server sent command: {command}")
            if command == "exit":
                break
            elif command == "sysinfo":
                client.send(get_system_info().encode())
            else:
                client.send("Unknown command".encode())
            client.send("OK".encode())
    except KeyboardInterrupt:
        print("Client shutting down...")
    finally:
        client.close()


if __name__ == '__main__':
    # Read the config file
    with open('config.json', 'r') as f:
        config = json.load(f)
    # Start the client
    start_client(config['host'], config['port'])

