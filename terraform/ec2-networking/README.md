# ORP EC2 Networking

This module provisions resources on AWS for EC2 networking assuming a database instance will be present in the system.

The module creates a VPC with two public subnets and an internet gateway.  A security group is also created for the database.

## Main

- Creates a VPC
- Creates resource "aws_security_group" "database_sg" - This is the security group for the instance
- Creates resource "aws_security_group_rule" "database_web_access" - This allows outbound access to internet resources
- Creates resource "aws_subnet" "public_subnet_db" - Creates the subnet for the DB
- Creates resource "aws_subnet" "public_subnet_aws_lb" - Creates the subnet for the Load Balancer
- Creates resource "aws_internet_gateway" "internet_gateway"
- Creates resource "aws_route_table" "public_route_table"
- Creates resource "aws_route" "public_route"
- Creates resource "aws_route_table_association" "public_subnet_db_route_table_association"
- Creates resource "aws_route_table_association" "public_subnet_aws_lb_route_table_association"

## Variables

- `base_name` - The base name of the stack.

## Outputs

- `vpc_id` - The ID of the main VPC for the stack
- `database_sg_id` - The ID of the security group for access to the database instance
- `database_subnet_id` - The ID of the subnet for the database instance
- `secondary_subnet_id` - The ID of the secondary subnet for the API load balancer