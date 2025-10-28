# TallerNoSQL

## Instalación
Crear cuenta influxdb, tomar nota de organización, url, y crear bucket y un con permisos de escritura y lectura. Crear archivo `.env` con los siguientes campos:

```
INFLUX_URL=<url>
INFLUX_ORG=<tu-org>
INFLUX_BUCKET=<tu-bucket>
INFLUX_TOKEN=<tu-token>
PERIOD_SEC=5
```

Luego, instala dependencias de `requirements.txt`, opcionalmente en un `venv` para facilitar deployment. Python 3 requerido.

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Correr

```
source .env
python3 influxdb_top.py
```

Recuerda correrlo dentro del venv si así lo instalaste.
