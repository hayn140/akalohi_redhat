variable "aws_region" {
  type    = string
  default = "us-east-2"
}

variable "import_ami_id" {
  type = string
  default = "ami-0fcb2d702e65ba9c1"
}

variable "ec2_instance_type" {
  type    = string
  default = "t3.micro"
}

variable "provisioned_ami_name" {
  type = string
  default = "rhel9-test-http-001"
}

variable "associate_public_ip" {
  type    = bool
  default = true
}

variable "ssh_timeout" {
  type    = string
  default = "10m"
}

variable "ec2_vpc_id" {
  type = string
  default = "vpc-0ed3e36b070ace94b"
}

variable "ec2_subnet_id" {
  type = string
  default = "subnet-0a9b05a2e34e52039"
}

variable "ssh_username" {
  type    = string
  default = "ec2-user"
}

