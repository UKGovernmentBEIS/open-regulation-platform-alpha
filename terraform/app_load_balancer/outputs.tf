output "api_target_arn" {
  description = "The ARN of the API load balancer target group"
  value       = aws_lb_target_group.api_target_group.arn
}