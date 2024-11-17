import argparse
import time
import base64
from dotenv import load_dotenv
import os
from confluent_kafka import Producer, Consumer, KafkaException

from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

from opentelemetry.instrumentation.confluent_kafka import (
    ConfluentKafkaInstrumentor,
    ProxiedConsumer,
    ProxiedProducer,
)
from opentelemetry.instrumentation.confluent_kafka.utils import (
    KafkaContextGetter,
    KafkaContextSetter,
)


def get_basic_auth_header(username, password):
    """Encodes the username and password to base64 for Basic Auth."""
    credentials = f"{username}:{password}"
    auth_bytes = base64.b64encode(credentials.encode("utf-8"))
    auth_header = auth_bytes.decode("utf-8")
    return f"Basic {auth_header}"


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(prog="service", description="Spin up new service")

    parser.add_argument("-i", "--inputs", nargs="*", required=True)
    parser.add_argument("-o", "--outputs", nargs="*", required=True)
    parser.add_argument("-d", "--delay", required=True)
    parser.add_argument("-n", "--name", required=True)
    parser.add_argument("-a", "--api")

    args = parser.parse_args()

    input_topics = args.inputs
    output_topics = args.outputs
    service_name = args.name
    span_name = service_name + "_span"
    delay = float(args.delay)

    # otel tracing
    resource = Resource(attributes={SERVICE_NAME: service_name})
    traceProvider = TracerProvider(resource=resource)
    trace.set_tracer_provider(traceProvider)
    tracer = trace.get_tracer("orc.tracer")

    user = os.getenv("LOGIT_USER")
    passw = os.getenv("LOGIT_SECRET")
    auth_header = get_basic_auth_header(user, passw)

    otlp_exporter = OTLPSpanExporter(
        "https://3061a777-1eb2-4870-bfaa-6ec53ccce86b-apm.logit.io:9082/v1/traces",
        headers={"Authorization": auth_header},
    )
    span_processor = BatchSpanProcessor(otlp_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)

    # kafka instrumentation
    instrumentation = ConfluentKafkaInstrumentor()

    conf = {
        "bootstrap.servers": "pkc-619z3.us-east1.gcp.confluent.cloud:9092",
        "security.protocol": "SASL_SSL",
        "sasl.mechanism": "PLAIN",
        "sasl.username": os.getenv("KAFKA_API_KEY"),
        "sasl.password": os.getenv("KAFKA_API_SECRET"),
        "group.id": "default",
    }

    # kafka consumer
    consumer = Consumer(conf)
    consumer = instrumentation.instrument_consumer(consumer)

    # kafka producer
    producer = Producer(conf)
    producer = instrumentation.instrument_producer(producer)

    def hyper_loop(consumer, producer, input_topics, output_topics):
        if input_topics:
            consumer.subscribe(input_topics)

        try:
            while True:
                msg = None
                if input_topics:
                    msg = consumer.poll(timeout=1.0)
                    if msg is None:
                        print("Nothing")
                        continue
                    if msg.error():
                        print(msg.error())
                        raise KafkaException(msg.error())
                if output_topics:
                    time.sleep(delay)
                for topic in output_topics or []:
                    if msg is None:
                        print("No message from input")
                    else:
                        producer.produce(topic, value=msg.value())
                        producer.flush()
                        print(f"forwarded value from {input_topics} to {topic}")

        except KeyboardInterrupt:
            print("Stopping Service")
        finally:
            consumer.close()

    with tracer.start_as_current_span("tracing orc"):
        hyper_loop(consumer, producer, input_topics, output_topics)


if __name__ == "__main__":
    main()
