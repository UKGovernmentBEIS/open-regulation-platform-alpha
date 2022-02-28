variable "base_name" {
  description = "The base name of the stack"
  type        = string
}

variable "database_sg_id" {
  description = "The ID of the security group for access to the database instance"
  type        = string
}

variable "database_subnet_id" {
  description = "The ID of the subnet in which to create the database instance"
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

variable "user_data" {
  description = "The script that will be run when the EC2 instance starts"
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
  default     = 100
}

variable "storage_iops" {
  description = "The IOPS to provision for the EBS volume used for database storage"
  type        = number
  default     = 3000
}

variable "version_tag" {
  description = "The ORP version being deployed"
  type        = string
}

variable "lockdown_access" {
  description = "Lockdown access to ports on the database instance"
  type        = bool
  default     = false
}