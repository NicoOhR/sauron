
provider "kubernetes" {
  config_path    = "~/.kube/config"
}
    
resource "kubernetes_deployment" "orc-gazgash" {
  metadata {
    name = "orc-gazgash"
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "orc-gazgash"
      }
    }

    template {
      metadata {
        labels = {
          app = "orc-gazgash"
        }
      }

      spec {
        container {
          name = "orc-gazgash"
          image = "nicoor/mock_service:v1.1"
          args = [ "-d", "0", "-i" ,  "-o" ,"gazbug","gazhorn","gazmuz","gazrat","gazthak" ]
          command = [ "python3", "main.py" ]
          env {
              name = "KAFKA_API_SECRET"
              value = var.kafka_api_secret
          }
          env {
              name = "KAFKA_API_KEY"
              value = var.kafka_api_key
          }
        }
      }
    }
  }
}
    
resource "kubernetes_deployment" "orc-gazbug" {
  metadata {
    name = "orc-gazbug"
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "orc-gazbug"
      }
    }

    template {
      metadata {
        labels = {
          app = "orc-gazbug"
        }
      }

      spec {
        container {
          name = "orc-gazbug"
          image = "nicoor/mock_service:v1.1"
          args = [ "-d", "0", "-i" , "gazgash", "-o" ,"gazrad","gazthak","gazluk" ]
          command = [ "python3", "main.py" ]
          env {
              name = "KAFKA_API_SECRET"
              value = var.kafka_api_secret
          }
          env {
              name = "KAFKA_API_KEY"
              value = var.kafka_api_key
          }
        }
      }
    }
  }
}
    
resource "kubernetes_deployment" "orc-gazhorn" {
  metadata {
    name = "orc-gazhorn"
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "orc-gazhorn"
      }
    }

    template {
      metadata {
        labels = {
          app = "orc-gazhorn"
        }
      }

      spec {
        container {
          name = "orc-gazhorn"
          image = "nicoor/mock_service:v1.1"
          args = [ "-d", "0", "-i" , "gazgash", "-o" ,"gazmog","gazmuz","gazluk" ]
          command = [ "python3", "main.py" ]
          env {
              name = "KAFKA_API_SECRET"
              value = var.kafka_api_secret
          }
          env {
              name = "KAFKA_API_KEY"
              value = var.kafka_api_key
          }
        }
      }
    }
  }
}
    
resource "kubernetes_deployment" "orc-gazmog" {
  metadata {
    name = "orc-gazmog"
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "orc-gazmog"
      }
    }

    template {
      metadata {
        labels = {
          app = "orc-gazmog"
        }
      }

      spec {
        container {
          name = "orc-gazmog"
          image = "nicoor/mock_service:v1.1"
          args = [ "-d", "0", "-i" , "gazhorn", "-o" ,"gazmuz","gazrad","gazthak","gazluk" ]
          command = [ "python3", "main.py" ]
          env {
              name = "KAFKA_API_SECRET"
              value = var.kafka_api_secret
          }
          env {
              name = "KAFKA_API_KEY"
              value = var.kafka_api_key
          }
        }
      }
    }
  }
}
    
resource "kubernetes_deployment" "orc-gazmuz" {
  metadata {
    name = "orc-gazmuz"
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "orc-gazmuz"
      }
    }

    template {
      metadata {
        labels = {
          app = "orc-gazmuz"
        }
      }

      spec {
        container {
          name = "orc-gazmuz"
          image = "nicoor/mock_service:v1.1"
          args = [ "-d", "0", "-i" , "gazgash","gazhorn","gazmog", "-o" ,"gazthak","gazluk" ]
          command = [ "python3", "main.py" ]
          env {
              name = "KAFKA_API_SECRET"
              value = var.kafka_api_secret
          }
          env {
              name = "KAFKA_API_KEY"
              value = var.kafka_api_key
          }
        }
      }
    }
  }
}
    
resource "kubernetes_deployment" "orc-gazrad" {
  metadata {
    name = "orc-gazrad"
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "orc-gazrad"
      }
    }

    template {
      metadata {
        labels = {
          app = "orc-gazrad"
        }
      }

      spec {
        container {
          name = "orc-gazrad"
          image = "nicoor/mock_service:v1.1"
          args = [ "-d", "0", "-i" , "gazbug","gazmog", "-o" ,"gazthak","gazlag" ]
          command = [ "python3", "main.py" ]
          env {
              name = "KAFKA_API_SECRET"
              value = var.kafka_api_secret
          }
          env {
              name = "KAFKA_API_KEY"
              value = var.kafka_api_key
          }
        }
      }
    }
  }
}
    
resource "kubernetes_deployment" "orc-gazrat" {
  metadata {
    name = "orc-gazrat"
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "orc-gazrat"
      }
    }

    template {
      metadata {
        labels = {
          app = "orc-gazrat"
        }
      }

      spec {
        container {
          name = "orc-gazrat"
          image = "nicoor/mock_service:v1.1"
          args = [ "-d", "0", "-i" , "gazgash", "-o" ,"gazthak" ]
          command = [ "python3", "main.py" ]
          env {
              name = "KAFKA_API_SECRET"
              value = var.kafka_api_secret
          }
          env {
              name = "KAFKA_API_KEY"
              value = var.kafka_api_key
          }
        }
      }
    }
  }
}
    
resource "kubernetes_deployment" "orc-gazthak" {
  metadata {
    name = "orc-gazthak"
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "orc-gazthak"
      }
    }

    template {
      metadata {
        labels = {
          app = "orc-gazthak"
        }
      }

      spec {
        container {
          name = "orc-gazthak"
          image = "nicoor/mock_service:v1.1"
          args = [ "-d", "0", "-i" , "gazgash","gazbug","gazmog","gazmuz","gazrad","gazrat", "-o"  ]
          command = [ "python3", "main.py" ]
          env {
              name = "KAFKA_API_SECRET"
              value = var.kafka_api_secret
          }
          env {
              name = "KAFKA_API_KEY"
              value = var.kafka_api_key
          }
        }
      }
    }
  }
}
    
resource "kubernetes_deployment" "orc-gazlag" {
  metadata {
    name = "orc-gazlag"
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "orc-gazlag"
      }
    }

    template {
      metadata {
        labels = {
          app = "orc-gazlag"
        }
      }

      spec {
        container {
          name = "orc-gazlag"
          image = "nicoor/mock_service:v1.1"
          args = [ "-d", "0", "-i" , "gazrad", "-o"  ]
          command = [ "python3", "main.py" ]
          env {
              name = "KAFKA_API_SECRET"
              value = var.kafka_api_secret
          }
          env {
              name = "KAFKA_API_KEY"
              value = var.kafka_api_key
          }
        }
      }
    }
  }
}
    
resource "kubernetes_deployment" "orc-gazluk" {
  metadata {
    name = "orc-gazluk"
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "orc-gazluk"
      }
    }

    template {
      metadata {
        labels = {
          app = "orc-gazluk"
        }
      }

      spec {
        container {
          name = "orc-gazluk"
          image = "nicoor/mock_service:v1.1"
          args = [ "-d", "0", "-i" , "gazbug","gazhorn","gazmog","gazmuz", "-o"  ]
          command = [ "python3", "main.py" ]
          env {
              name = "KAFKA_API_SECRET"
              value = var.kafka_api_secret
          }
          env {
              name = "KAFKA_API_KEY"
              value = var.kafka_api_key
          }
        }
      }
    }
  }
}
    