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
  project = "terraform-demo-411919"
  region  = "us-central1"
}


# resource "the_resource_name" "variable-name"
resource "google_storage_bucket" "test-bucket" {
  name          = "terraform-demo-411919-terraform-testing-bucket"
  location      = "US"
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

