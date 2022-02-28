variable "base_name" {
  description = "The base name of the stack"
  type        = string
}

variable "vpc_id" {
  description = "The ID of the VPC for the stack"
  type        = string
}

variable "subnet_ids" {
  description = "The IDs for the subnets to use for the API load balancer"
  type        = list(string)
}

variable "database_sg_id" {
  description = "The ID of the security group for access to the database instance"
  type        = string
}

variable "domain" {
  description = "The domain for the API"
  type        = string
}

variable "subdomain" {
  description = "The subdomain for the API"
  type        = string
  default     = "api"
}

variable "instance_port" {
  description = "The port that should be exposed via the API load balancer"
  type        = number
  default     = 443
}

variable "health_check_path" {
  description = "The path that should be used to check the health of the API load balancer"
  type        = string
  default     = "/"
}

variable "instance_id" {
  description = "The instance ID of the EC2 instance"
  type        = string
}