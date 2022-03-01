data "aws_region" "current" {}

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags                 = {}
}

resource "aws_security_group" "database_sg" {
  name        = "${var.base_name}-database"
  description = "Rules for access to the ${var.base_name} database"
  vpc_id      = aws_vpc.main.id
  tags        = {}
}

resource "aws_security_group_rule" "database_web_access" {
  type              = "egress"
  description       = "Outbound access to internet resources"
  from_port         = 0
  to_port           = 0
  protocol          = "all"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.database_sg.id
  ipv6_cidr_blocks  = []
  prefix_list_ids   = []
}

resource "aws_subnet" "public_subnet_db" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.0.0/24"
  availability_zone       = "${data.aws_region.current.name}a"
  map_public_ip_on_launch = true
  tags                    = {}
}

resource "aws_subnet" "public_subnet_aws_lb" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.100.0/24"
  availability_zone       = "${data.aws_region.current.name}b"
  map_public_ip_on_launch = true
  tags                    = {}
}

resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.main.id
  tags   = {}
}

resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.main.id
  tags   = {}
}

resource "aws_route" "public_route" {
  route_table_id         = aws_route_table.public_route_table.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.internet_gateway.id
}

resource "aws_route_table_association" "public_subnet_db_route_table_association" {
  subnet_id      = aws_subnet.public_subnet_db.id
  route_table_id = aws_route_table.public_route_table.id
}

resource "aws_route_table_association" "public_subnet_aws_lb_route_table_association" {
  subnet_id      = aws_subnet.public_subnet_aws_lb.id
  route_table_id = aws_route_table.public_route_table.id
}