import os
import time
import socket
import psutil
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from datetime import datetime, timezone

def leer_cpu():
    """Devuelve el uso promedio de CPU (%) en 1 segundo."""
    return psutil.cpu_percent(interval=1)

def leer_memoria():
    """Devuelve {'used_mb': float, 'percent': float}."""
    mem = psutil.virtual_memory()
    used_mb = mem.used / 1024**2
    return {"used_mb": used_mb, "percent": mem.percent}

def construir_punto(cpu, mem, hostname, osver):
    """Crea un punto InfluxDB con las métricas de CPU y memoria."""
    point = (
        Point("sys_metrics")
        .tag("hostname", hostname)
        .tag("os", osver)
        .field("cpu_percent", float(cpu))
        .field("mem_used_mb", float(mem["used_mb"]))
        .field("mem_percent", float(mem["percent"]))
        .time(datetime.now(timezone.utc), WritePrecision.NS)
    )
    return point

def main():
    load_dotenv()

    # Configuración desde .env
    token = os.getenv("INFLUX_TOKEN")
    org = os.getenv("INFLUX_ORG")
    bucket = os.getenv("INFLUX_BUCKET")
    url = os.getenv("INFLUX_URL")
    period = int(os.getenv("PERIOD_SEC", 5))

    hostname = socket.gethostname()
    osver = os.uname().sysname

    client = InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api()

    print(f"Iniciando captura en {hostname} cada {period}s...")
    while True:
        cpu = leer_cpu()
        mem = leer_memoria()
        point = construir_punto(cpu, mem, hostname, osver)
        write_api.write(bucket=bucket, org=org, record=point)
        print(f"{datetime.now()}: CPU={cpu:.2f}%, MEM={mem['percent']:.2f}%")
        time.sleep(period)

if __name__ == "__main__":
    main()
