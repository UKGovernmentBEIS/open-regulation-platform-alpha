output "database_dns" {
  description = "The DNS address of the elastic IP"
  value       = module.database.database_dns
}