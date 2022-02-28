variable "aws_region" {
  description = "The AWS region under which to deploy the stack"
  type = string
}

variable "artifact_bucket" {
  description = "The bucket containing build artifacts"
  type        = string
  default     = "orp-build-outputs"
}

variable "base_name" {
  description = "The base name for the stack"
  type        = string
}

variable "version_tag" {
  description = "The orp version being deployed"
  type        = string
}

variable "domain" {
  description = "The domain for the cloudfront distribution"
  type        = string
}

variable "web_subdomain" {
  default     = "www"
  description = "The subdomain for the cloudfront distribution"
  type        = string
}

variable "api_subdomain" {
  default     = "api"
  description = "The subdomain for the API"
  type        = string
}

variable "users_subdomain" {
  default     = "users"
  description = "The subdomain for the user admin API"
  type        = string
}

variable "app_name" {
  description = "The name for the application"
  type        = string
}

variable "ssh_key_name" {
  description = "The name of the SSH key to be granted access to the database instance"
  type        = string
}

variable "private_ssh_key_path" {
  description = "The path to the private SSH key with access to the database instance"
  type        = string
}

variable "ami_id" {
  description = "The ID of the AMI to use for the database instance"
  type        = string
  default     = "ami-050949f5d3aede071"
}

variable "instance_type" {
  description = "The type of the EC2 instance used for the database"
  type        = string
  default     = "t3.medium"
}

variable "storage_type" {
  description = "The type of the EBS volume used for database storage"
  type        = string
  default     = "gp3"
}

variable "storage_gb" {
  description = "The size in GB of the EBS volume used for database storage"
  type        = number
  default     = 2000
}

variable "storage_iops" {
  description = "The IOPS to provision for the EBS volume used for database storage"
  type        = number
  default     = 16000
}

variable "storage_throughput" {
  description = "The throughput to provision for the EBS volume used for database storage, only applies to gp3 storage"
  type        = string
  default     = 1000
}

variable "database" {
  description = "The database name to use for the application"
  type        = string
}

variable "lockdown_access" {
  description = "Lockdown access to ports on the database instance"
  type        = bool
  default     = false
}