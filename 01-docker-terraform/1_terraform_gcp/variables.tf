variable "credentials" {
  description = "Credentials"
  default     = "./keys/credentials.json"
}

variable "project" {
  description = "Project"
  default     = "terraform-demo-411919"

}

variable "region" {
  description = "Project Location"
  default     = "us-central1"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}

variable "bq_dataset_name" {
  description = "BigQuery Dataset Name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "Storage Bucket Name"
  default     = "terraform-demo-411919-terraform-testing-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}


