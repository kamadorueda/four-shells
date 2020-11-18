resource "aws_internet_gateway" "four_shells" {
  tags = {
    "Name" = "4shells"
    "management:product" = "4shells"
  }
  vpc_id = aws_vpc.four_shells.id
}

resource "aws_route" "four_shells" {
  destination_cidr_block = "0.0.0.0/0"
  gateway_id = aws_internet_gateway.four_shells.id
  route_table_id = aws_vpc.four_shells.default_route_table_id
}

resource "aws_route_table" "public" {
  tags = {
    "Name" = "4shells"
    "management:product" = "4shells"
  }
  vpc_id = aws_vpc.four_shells.id
}

resource "aws_route_table_association" "public_1" {
  route_table_id = aws_route_table.public.id
  subnet_id = aws_subnet.public_1.id
}

resource "aws_subnet" "public_1" {
  availability_zone = "${var.region}a"
  cidr_block = "192.168.0.0/24"
  tags = {
    "Name" = "4shells"
    "management:product" = "4shells"
  }
  vpc_id = aws_vpc.four_shells.id
}

resource "aws_vpc" "four_shells" {
  assign_generated_ipv6_cidr_block = false
  cidr_block = "192.168.0.0/16"
  enable_classiclink = false
  enable_classiclink_dns_support = false
  enable_dns_hostnames = false
  enable_dns_support = true
  instance_tenancy = "default"
  tags = {
    "Name" = "4shells"
    "management:product" = "4shells"
  }
}
