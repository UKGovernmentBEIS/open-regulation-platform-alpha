output "vpc_id" {
  description = "The ID of the main VPC for the stack"
  value       = aws_vpc.main.id
}

output "database_sg_id" {
  description = "The ID of the security group for access to the database instance"
  value       = aws_security_group.database_sg.id
}

output "database_subnet_id" {
  description = "The ID of the subnet for the database instance"
  value       = aws_subnet.public_subnet_db.id
}

output "secondary_subnet_id" {
  description = "The ID of the secondary subnet for the API load balancer"
  value       = aws_subnet.public_subnet_aws_lb.id
}