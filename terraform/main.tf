terraform {
  backend "s3" {
    workspace_key_prefix = "terraform-envs"
    key                  = "terraform-state"
    region               = "eu-west-2"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.74.3"
    }
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      TerraformStack = var.base_name
    }
  }
}

data "aws_caller_identity" "current" {}

module "ec2_networking" {
  source    = "./ec2-networking"
  base_name = var.base_name
}

module "database" {
  source               = "./database"
  base_name            = var.base_name
  database_sg_id       = module.ec2_networking.database_sg_id
  database_subnet_id   = module.ec2_networking.database_subnet_id
  ami_id               = var.ami_id
  storage_type         = var.storage_type
  storage_gb           = var.storage_gb
  storage_iops         = var.storage_iops
  ssh_key_name         = var.ssh_key_name
  private_ssh_key_path = var.private_ssh_key_path
  version_tag          = var.version_tag
  lockdown_access      = var.lockdown_access
  user_data = file("./database/user_data.tpl")
}

resource "null_resource" "git_checkout" {
  connection {
    user        = "admin"
    host        = module.database.database_ip
    type        = "ssh"
    private_key = file(var.private_ssh_key_path)
  }

  provisioner "file" {
    source      = "id_rsa.pub"
    destination = "/home/admin/.ssh/id_rsa.pub"
  }

  provisioner "file" {
    source      = "id_rsa"
    destination = "/home/admin/.ssh/id_rsa"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod 400 ~/.ssh/id_rsa",
      "ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts",
      "git clone git@github.com:UKGovernmentBEIS/open-regulation-platform-alpha.git"
    ]
  }

  depends_on = [
    module.ec2_networking,
    module.database
  ]
}

resource "null_resource" "deployment" {
  connection {
    user        = "admin"
    host        = module.database.database_ip
    type        = "ssh"
    private_key = file(var.private_ssh_key_path)
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x ~/open-regulation-platform-alpha/api_demo/demo_installs.sh",
      "sudo apt-get install -y python3-pip",
      "cd open-regulation-platform-alpha",
      "./deploy.sh"
    ]
  }

  depends_on = [
    module.ec2_networking,
    module.database,
    null_resource.git_checkout
  ]
}

module "app_load_balancer" {
  source    = "./app_load_balancer"
  base_name = var.base_name
  vpc_id    = module.ec2_networking.vpc_id
  domain    = var.domain
  subdomain = var.api_subdomain
  subnet_ids = [
    module.ec2_networking.database_subnet_id,
    module.ec2_networking.secondary_subnet_id
  ]
  database_sg_id = module.ec2_networking.database_sg_id
  instance_id = module.database.database_instance_id

  depends_on = [
    null_resource.deployment
  ]
}
