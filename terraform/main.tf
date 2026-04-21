variable "GROQ_API_KEY" {}

terraform {
  backend "s3" {
    bucket = "terraform-state-atisha"
    key    = "terraform.tfstate"
    region = "ap-south-1"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-south-1"
}

resource "aws_instance" "telecom" {
  ami           = "ami-0e670eb768a5fc3d4"
  instance_type = "t3.micro"

  tags = {
    Name = "telecom-server"
  }

  user_data = <<-EOF
              #!/bin/bash
              sudo apt update -y
              sudo apt install docker.io -y
              sudo systemctl start docker
              sudo systemctl enable docker

              sudo docker run -d -p 8000:8000 -e GROQ_API_KEY=${var.GROQ_API_KEY} telecom-app
              EOF
}

output "public_ip" {
  value = aws_instance.telecom.public_ip
}
