data "aws_region" "current" {}

data "http" "public_ip" {
  url = "https://ipv4.icanhazip.com/"
}

resource "aws_security_group_rule" "database_deployment_ssh_access" {
  count             = var.lockdown_access ? 0 : 1
  type              = "ingress"
  description       = "Deployment access"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["${chomp(data.http.public_ip.body)}/32"]
  security_group_id = var.database_sg_id
  ipv6_cidr_blocks  = []
  prefix_list_ids   = []
}

resource "aws_security_group_rule" "database_deployment_ssh_access_office" {
  count             = var.lockdown_access ? 0 : 1
  type              = "ingress"
  description       = "SSH Access from AE Office"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["81.137.67.60/32"]
  security_group_id = var.database_sg_id
  ipv6_cidr_blocks  = []
  prefix_list_ids   = []
}

resource "aws_instance" "database" {
  instance_type          = var.instance_type
  availability_zone      = "${data.aws_region.current.name}a"
  vpc_security_group_ids = [var.database_sg_id]
  key_name               = var.ssh_key_name
  subnet_id              = var.database_subnet_id
  ami                    = var.ami_id

  root_block_device {
    iops        = var.storage_iops
    volume_size = var.storage_gb
    volume_type = var.storage_type
    tags        = {}
  }

  user_data = var.user_data

  tags = {
    Name = "${var.base_name}-database"
  }

}

resource "aws_eip" "database_ip" {
  tags = {}
}

resource "aws_eip_association" "database_eip_association" {
  instance_id   = aws_instance.database.id
  allocation_id = aws_eip.database_ip.id

  provisioner "remote-exec" {
    inline = ["cloud-init status --wait > /dev/null 2>&1"]

    connection {
      user        = "admin"
      host        = self.public_ip
      type        = "ssh"
      private_key = file(var.private_ssh_key_path)
    }
  }
}

resource "aws_s3_bucket" "data_bucket" {
  bucket = "${var.base_name}-data"
}


resource "null_resource" "docker_install" {
  connection {
    user        = "admin"
    host        = aws_eip_association.database_eip_association.public_ip
    type        = "ssh"
    private_key = file(var.private_ssh_key_path)
  }

  provisioner "file" {
    destination = "/opt/orp/docker_install.sh"
    content = templatefile("database/docker_install.sh", {})
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /opt/orp/docker_install.sh",
      "/opt/orp/docker_install.sh",
    ]
  }

  triggers = {
    file_hash   = filesha256("database/docker_install.sh")
    instance_id = aws_instance.database.id
  }
}
