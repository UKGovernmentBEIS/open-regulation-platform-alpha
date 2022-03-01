# ORP EC2 Database

This module provisions resources on AWS for an EC2 instance.

## Main

- Get public IP
- Creates resource "aws_security_group_rule" "database_deployment_ssh_access" - This will allow your IP to ssh onto the machine
- Creates resource "aws_security_group_rule" "database_deployment_ssh_access_office" - This will allow the AE office IP to ssh onto the machine
- Creates resource "aws_instance" "database" - This creates the EC2 instance
- Creates resource "aws_eip_association" "database_eip_association" - This associates the elastic IP address with the instance
- Runs docker_install - This installs docker onto the instance

## Variables

- `base_name` - The base name of the stack.
- `database_sg_id` - The ID of the security group for access to the database instance.
- `database_subnet_id` - The ID of the subnet in which to create the database instance.
- `ssh_key_name` - The name of the SSH key to be granted access to the database instance.
- `private_ssh_key_path` - The path to the private SSH key with access to the database instance.
- `user_data` - The script that will be run when the EC2 instance starts.
- `ami_id` - The ID of the AMI to use for the database instance, default is "ami-050949f5d3aede071".
- `instance_type` - The type of the EC2 instance used for the database, default is "t3.medium".
- `storage_type` - The type of the EBS volume used for database storage, default is "gp3".
- `storage_gb` - The size in GB of the EBS volume used for database storage, default is 100.
- `storage_iops` - The IOPS to provision for the EBS volume used for database storage, default is 3000.
- `version_tag` - The ORP version being deployed.
- `lockdown_access` - Lockdown access to ports on the database instance, default is false.

## Outputs

- `database_ip` - The IP address of the database instance
- `elastic_ip_id` - The id of the elastic IP association
- `data_bucket` - The name of the data bucket created
- `database_dns` - The DNS of the database instance
- `database_instance_id` - The id of the instance
