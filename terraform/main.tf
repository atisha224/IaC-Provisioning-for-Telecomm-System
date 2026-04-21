provider "aws" {
  region = "ap-south-1"
}

resource "aws_instance" "telecom" {
  ami           = "ami-0f58b397bc5c1f2e8"
  instance_type = "t3.micro"

  tags = {
    Name = "telecom-server"
  }
}

output "public_ip" {
  value = aws_instance.telecom.public_ip
}
