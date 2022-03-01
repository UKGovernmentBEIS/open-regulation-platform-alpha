output "database_ip" {
  description = "The IP address of the database instance"
  value       = aws_eip_association.database_eip_association.public_ip
}

output "elastic_ip_id" {
  description = "The id of the elastic IP association"
  value       = aws_eip_association.database_eip_association.id
}

output "data_bucket" {
  description = "The name of the data bucket"
  value       = aws_s3_bucket.data_bucket.id
}

output "database_dns" {
  description = "The DNS address of the elastic IP"
  value       = aws_eip.database_ip.public_dns
}

output "database_instance_id" {
  description = "The Instance ID of the database instance"
  value       = aws_instance.database.id
}