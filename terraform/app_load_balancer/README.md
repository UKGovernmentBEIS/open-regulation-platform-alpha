# ORP Application Load Balancer

This module provisions resources on AWS, including an application load balancer, to provide access to an EC2 instance.  The module also creates and validates a certificate for the API.

## Main

- Creates resource "aws_security_group" "api_load_balancer_sg" - This creates a security group for the load balancer
- Creates resource "aws_security_group_rule" "api_public_access" - This SG rule allows inbound access to the API load balancer
- Creates resource "aws_security_group_rule" "api_container_access" - This SG rule allows outbound access to API containers
- Creates resource "aws_security_group_rule" "api_container_access_all_ports" - This SG rule allows outbound access to API containers All Ports
- Creates resource "aws_security_group_rule" "database_deployment_lb_health_check" - This SG rule is for the LB-Health Check
- Creates resource "aws_security_group_rule" "database_deployment_lb_api" - This SG rule is for the LB-API
- Creates resource "aws_security_group_rule" "database_deployment_lb_editorial_ui" - This SG rule is for the LB-Editorial-UI
- Creates resource "aws_s3_bucket" "logs_bucket" - This bucket will contain the logs for the instance
- Creates resource "aws_s3_bucket_policy" "policy" - This assigns the policy defined below to the S3 bucket
- Creates data "aws_iam_policy_document" "s3_bucket_lb_write" - This is the policy for the S3 bucket
- Creates resource "aws_lb" "api_load_balancer"
- Creates resource "aws_lb_target_group" "api_target_group"
- Creates resource "aws_lb_target_group" "ui_target_group"
- Creates resource "aws_lb_target_group" "rpc_target_group"
- Creates resource "aws_route53_record" "api_alias" - Creates the alias for the API
- Creates resource "aws_route53_record" "certificate_validation"
- Creates resource "aws_acm_certificate" "certificate"
- Creates resource "aws_acm_certificate_validation" "acm_validation"
- Creates resource "aws_lb_listener_certificate" "listener_cert"
- Creates resource "aws_lb_listener" "api_listener" - This creates the default listener to redirect to the UI target group
- Creates resource "aws_lb_listener_rule" "rpc_forwarding" - This creates the listener to forward to the RPC target group
- Creates resource "aws_lb_listener_rule" "api_forwarding" - This creates the listener to forward to the API target group

## Variables

- `base_name` - The base name of the stack.
- `vpc_id` - The ID of the VPC for the stack.
- `subnet_ids` - The IDs for the subnets to use for the API load balancer.
- `database_sg_id` - The ID of the security group for access to the database instance
- `domain` - The domain for the API.
- `subdomain` - The subdomain for the API, default is "api".
- `instance_port` - The port that should be exposed via the API load balancer, default is 443.
- `health_check_path` - The path that should be used to check the health of the API load balancer, default is "/".
- `instance_id` - The instance ID of the EC2 instance

## Outputs

- `api_target_arn` - The ARN of the API load balancer target group.
