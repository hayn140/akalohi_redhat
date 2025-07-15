packer {
  required_plugins {
    amazon = {
      source  = "github.com/hashicorp/amazon"
      version = ">= 1.0.0"
    }
    ansible = {
      source  = "github.com/hashicorp/ansible"
      version = ">= 1.0.0"
    }
  }
}

source "amazon-ebs" "rhel" {
  region                              = var.aws_region
  source_ami                          = var.import_ami_id
  instance_type                       = var.ec2_instance_type
  ssh_username                        = var.ssh_username
  ami_name                            = var.provisioned_ami_name
  associate_public_ip_address         = var.associate_public_ip
  ssh_timeout                         = var.ssh_timeout
  vpc_id                              = var.ec2_vpc_id
  subnet_id                           = var.ec2_subnet_id

  communicator                        = "ssh"

  run_tags = {
    Name        = "packer-provisioning-instance"
    Environment = "build"
  }

}

build {
  sources = ["source.amazon-ebs.rhel"]

  provisioner "ansible" {
    use_proxy        = false
    playbook_file    = "./playbook.yml"
  }
}
