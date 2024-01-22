terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6.0"

    }
  }
}

provider "google" {
  # credentials = "credentials_path" # not best practice
  credentials = file(var.credentials)
  # using env
  # export GOOGLE_CREDENTIALS="/home/pedro/de-camp-24/01-docker-terraform/1_terraform_gcp/keys/credentials.json"
  project = var.project
  region  = var.region
}


## Bucket
# resource "the_resource_name" "variable-name"
resource "google_storage_bucket" "test-bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      # age in days
      age = 3
    }
    action {
      type = "Delete"
    }
  }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

## bigquery

resource "google_bigquery_dataset" "demo_dataset_resource" {
  dataset_id = var.bq_dataset_name
  # friendly_name               = "test"
  # description                 = "This is a test description"
  # location                    = "EU"
  # default_table_expiration_ms = 3600000
}
