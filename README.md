**README.md**



# Tokoin Hospital — Data Warehouse Pipeline

Big Data pipeline for Tokoin Hospital (Lomé, Togo).
Covers multi-source ingestion, PostgreSQL DWH, MongoDB dossiers, Kafka streaming and Metabase dashboards.

---

## Prerequisites

- [Docker](https://www.docker.com/) & Docker Compose
- Python 3.10+

---

## 1. Clone the repository

```bash
git clone https://github.com/taoufikOURO/tokoin-hospital-dwh.git
cd tokoin-hospital-dwh
```

## 2. Configure environment variables

Copy the example file and fill in your values :

```bash
cp .env.example .env
```

Edit `.env` with your credentials (see `.env.example` for reference).

> **Check ports** : the default ports used are `5431` (PostgreSQL), `27016` (MongoDB), `3000` (Metabase), `9092` (Kafka), `2181` (Zookeeper). If any of these are already in use on your machine, change them in both `docker-compose.yml` and `.env`.

---

## 3. Start Docker services

```bash
docker compose up -d
```

Wait about 30 seconds for all services to be ready, then verify :

```bash
docker ps
```

All 5 containers should be running : `hospital_postgres`, `hospital_mongodb`, `hospital_metabase`, `kafka`, `zookeeper`.

---

## 4. Check source data files

Make sure the following files are present in `data/files/` :

```
data/files/
├── patients.xml
├── medecins.xlsx
├── services.csv
├── consultations.txt
├── medicaments.csv
├── analyses.csv
└── urgences.json
```

---

## 5. Install Python dependencies

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

---

## 6. Run the pipeline

```bash
python main.py
```

`main.py` runs the full pipeline in order :

| Function                       | Description                                                  |
| ------------------------------ | ------------------------------------------------------------ |
| `load_all()`                 | Loads all source files into the PostgreSQL staging tables    |
| `transform_all()`            | Builds dimensions and `fact_consultations`(Data Warehouse) |
| `export_dossiers_patients()` | Exports enriched patient dossiers to MongoDB                 |
| `run_mongo_queries()`        | Runs analytical aggregation pipelines on MongoDB             |

---

## 7. Access Metabase

Open [http://localhost:3000](http://localhost:3000/) and connect to the `dwh` schema on PostgreSQL to explore the dashboards.

---

## 8. Kafka producer (optional)

To simulate the real-time urgency stream :

```bash
python kafka_producer.py
```

---

## Project structure

```
hospital-dwh/
├── main.py
├── docker-compose.yml
├── kafka_producer.py
├── config/config.py
├── connections/
├── data/
│   ├── files/          ← source data files
│   ├── requests/       ← SQL scripts
│   └── loader.py
└── processing/
    ├── transformer.py
    ├── mongo_export.py
    └── mongo_queries.py
```
