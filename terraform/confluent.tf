# Configure the Confluent Provider
terraform {
  required_providers {
    confluent = {
      source  = "confluentinc/confluent"
      version = "2.9.0"
    }
  }
}


# confluent config
provider "confluent" {
  cloud_api_key       = var.confluent_cloud_api_key              # optionally use KAFKA_API_KEY env var
  cloud_api_secret    = var.confluent_cloud_api_secret           # optionally use KAFKA_API_SECRET env var

  // kafka
  kafka_id            = var.kafka_id
  kafka_rest_endpoint = var.kafka_rest_endpoint
  kafka_api_key       = var.kafka_api_key
  kafka_api_secret    = var.kafka_api_secret

  // schema registry
  schema_registry_api_key       = var.schema_registry_api_key       # optionally use SCHEMA_REGISTRY_API_KEY env var
  schema_registry_api_secret    = var.schema_registry_api_secret
  schema_registry_id            = var.kafka_id
  schema_registry_rest_endpoint = var.kafka_rest_endpoint
}


# kafka topics
resource "confluent_kafka_topic" "zipkin" {
    topic_name = "zipkin"
}

# service accounter
resource "confluent_service_account" "producer" {
  display_name = "producer"
  description  = "generic producer service account to go fast"
}

resource "confluent_kafka_acl" "produce-write-stonks" {
  resource_type = "TOPIC"
  resource_name = "*"
  pattern_type  = "LITERAL"
  host          = "*"
  principal     = "User:${confluent_service_account.producer.id}"
  operation     = "WRITE"
  permission    = "ALLOW"
}
