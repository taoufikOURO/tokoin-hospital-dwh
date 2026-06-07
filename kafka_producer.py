from kafka import KafkaProducer
from config.config import KAFKA_BROKER, KAFKA_TOPIC, DATA_DIR
import json
import time

def produce_urgences():
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    with open(f"{DATA_DIR}/urgences.json", encoding="utf-8") as f:
        urgences = json.load(f)

    for u in urgences:
        producer.send(KAFKA_TOPIC, value=u)
        print(f"[KAFKA] Envoyé : {u['urgence_id']}")
        time.sleep(0.1)

    producer.flush()
    print(f"[OK] {len(urgences)} urgences envoyées dans Kafka.")

if __name__ == "__main__":
    produce_urgences()