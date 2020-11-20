data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "admin" {
  statement {
    effect = "Allow"
    actions = [
      "autoscaling:*",
      "dynamodb:*",
      "ec2:*",
      "ecr:*",
      "ecs:*",
      "elasticloadbalancing:*",
      "iam:*",
      "logs:*",
      "s3:*",
    ]
    resources = ["*"]
  }
}

data "aws_iam_policy_document" "ecs" {
  statement {
    actions = ["sts:AssumeRole"]
    effect = "Allow"
    principals {
      identifiers = [
        "ecs.amazonaws.com",
        "ec2.amazonaws.com",
      ]
      type = "Service"
    }
  }
}

data "aws_iam_policy_document" "ecs_instance" {
  statement {
    actions = [
      "cloudwatch:*",
      "ecs:*",
      "ec2:*",
      "elasticloadbalancing:*",
      "s3:*",
      "logs:*",
    ]
    effect = "Allow"
    resources = ["*"]
  }
}

data "aws_iam_policy_document" "ecs_service" {
  statement {
    actions = [
      "elasticloadbalancing:Describe*",
      "elasticloadbalancing:DeregisterInstancesFromLoadBalancer",
      "elasticloadbalancing:DeregisterTargets",
      "elasticloadbalancing:RegisterInstancesWithLoadBalancer",
      "elasticloadbalancing:RegisterTargets",
      "ec2:AuthorizeSecurityGroupIngress",
      "ec2:Describe*",
    ]
    effect = "Allow"
    resources = ["*"]
  }
}

output "admin_key" {
  sensitive = true
  value = aws_iam_access_key.admin.id
}

output "admin_secret" {
  sensitive = true
  value = aws_iam_access_key.admin.secret
}

provider "aws" {
  access_key = var.access_key
  secret_key = var.secret_key
  region = var.region
}

resource "aws_alb_target_group" "four_shells" {
  health_check {
    path = "/ping"
    matcher = "200"
  }
  name = "4shells"
  port = 80
  protocol = "HTTP"
  tags = {
    "management:product" = "4shells"
    "Name" = "4shells"
  }
  vpc_id = aws_vpc.four_shells.id
}

resource "aws_alb_listener" "four_shells" {
  default_action {
    type = "forward"
    target_group_arn = aws_alb_target_group.four_shells.arn
  }
  depends_on = [
    aws_alb_target_group.four_shells,
  ]
  load_balancer_arn = aws_lb.four_shells.id
  port = "80"
  protocol = "HTTP"
}

resource "aws_autoscaling_group" "four_shells" {
  desired_capacity = 1
  health_check_type = "EC2"
  launch_configuration = aws_launch_configuration.four_shells.name
  max_size = 1
  min_size = 0
  name = "4shells"
  tags = [
    {
      key = "Name"
      propagate_at_launch = false
      value = "4shells"
    },
    {
      key = "management:product"
      propagate_at_launch = false
      value = "4shells"
    },
  ]
  vpc_zone_identifier = [
    aws_subnet.public_a.id,
    aws_subnet.public_b.id,
  ]
}

resource "aws_cloudwatch_log_group" "four_shells" {
  name = "/ecs/4shells"
  retention_in_days = 1
  tags = {
    "management:product" = "4shells"
    "Name" = "4shells"
  }
}

resource "aws_cloudwatch_log_stream" "four_shells" {
  log_group_name = aws_cloudwatch_log_group.four_shells.name
  name = "4shells"
}

resource "aws_ecs_cluster" "four_shells" {
  name = "4shells"
  tags = {
    "management:product" = "4shells"
    "Name" = "4shells"
  }
}

resource "aws_ecs_service" "four_shells" {
  cluster = aws_ecs_cluster.four_shells.id
  depends_on = [
    aws_alb_listener.four_shells,
    aws_iam_role_policy.ecs_service,
  ]
  desired_count = 1
  force_new_deployment = true
  iam_role = aws_iam_role.ecs_service.arn
  load_balancer {
    target_group_arn = aws_alb_target_group.four_shells.arn
    container_name = "4shells"
    container_port = 8400
  }
  name = "4shells"
  tags = {
    "management:product" = "4shells"
    "Name" = "4shells"
  }
  task_definition = aws_ecs_task_definition.four_shells.arn
}

resource "aws_ecs_task_definition" "four_shells" {
  container_definitions = jsonencode([
    {
      command = [
        "4shells"
      ]
      cpu = 1
      environment = [
      ]
      essential = true
      image = "docker.pkg.github.com/kamadorueda/4shells.com/4shells.com:latest"
      links = []
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group = aws_cloudwatch_log_group.four_shells.name
          awslogs-region = var.region
          awslogs-stream-prefix = aws_cloudwatch_log_stream.four_shells.name
        }
      }
      memory = 900
      name = "4shells"
      portMappings = [
        {
          containerPort = 8400
          hostPort = 0
          protocol = "tcp"
        }
      ]
    },
  ])
  family = "4shells"
  tags = {
    "management:product" = "4shells"
    "Name" = "4shells"
  }
}

resource "aws_iam_access_key" "admin" {
  user = aws_iam_user.admin.name
  status = "Active"
}

resource "aws_iam_instance_profile" "ecs" {
  name = "ecs"
  role = aws_iam_role.ecs.name
}

resource "aws_iam_policy" "admin" {
  name = "admin"
  policy = data.aws_iam_policy_document.admin.json
}

resource "aws_iam_role" "ecs" {
  assume_role_policy = data.aws_iam_policy_document.ecs.json
  name = "ecs"
  tags = {
    "management:product" = "4shells"
    "Name" = "ecs"
  }
}

resource "aws_iam_role" "ecs_service" {
  assume_role_policy = data.aws_iam_policy_document.ecs.json
  name = "ecs_service"
  tags = {
    "management:product" = "4shells"
    "Name" = "ecs_service"
  }
}

resource "aws_iam_role_policy" "ecs_instance" {
  name = "ecs_instance"
  policy = data.aws_iam_policy_document.ecs_instance.json
  role = aws_iam_role.ecs.id
}

resource "aws_iam_role_policy" "ecs_service" {
  name = "ecs_service_role_policy"
  policy = data.aws_iam_policy_document.ecs_service.json
  role = aws_iam_role.ecs_service.id
}

resource "aws_iam_user" "admin" {
  name = "admin"
  tags = {
    "management:product" = "4shells"
    "Name" = "admin"
  }
}

resource "aws_iam_user_policy_attachment" "admin" {
  user = "admin"
  policy_arn = aws_iam_policy.admin.arn
}

resource "aws_internet_gateway" "four_shells" {
  tags = {
    "management:product" = "4shells"
    "Name" = "4shells"
  }
  vpc_id = aws_vpc.four_shells.id
}

resource "aws_launch_configuration" "four_shells" {
  associate_public_ip_address = true
  iam_instance_profile = aws_iam_instance_profile.ecs.name
  image_id = "ami-088beb3aba8c353f1"
  instance_type = "t2.micro"
  name = "4shells"
  security_groups = [
    aws_security_group.four_shells_ecs.id,
  ]
  user_data = file("${path.module}/ecs_user_data.sh")
}

resource "aws_lb" "four_shells" {
  internal = false
  load_balancer_type = "application"
  name = "4shells"
  security_groups = [
    aws_security_group.four_shells_lb.id,
  ]
  subnets = [
    aws_subnet.public_a.id,
    aws_subnet.public_b.id,
  ]
  tags = {
    "management:product" = "4shells"
    "Name" = "4shells"
  }
}

resource "aws_route" "four_shells" {
  destination_cidr_block = "0.0.0.0/0"
  gateway_id = aws_internet_gateway.four_shells.id
  route_table_id = aws_vpc.four_shells.default_route_table_id
}

resource "aws_route_table" "public" {
  tags = {
    "management:product" = "4shells"
    "Name" = "public"
  }
  vpc_id = aws_vpc.four_shells.id
}

resource "aws_route_table_association" "public_a" {
  route_table_id = aws_route_table.public.id
  subnet_id = aws_subnet.public_a.id
}

resource "aws_route_table_association" "public_b" {
  route_table_id = aws_route_table.public.id
  subnet_id = aws_subnet.public_b.id
}

resource "aws_security_group" "four_shells_lb" {
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  name = "four_shells_lb"
  tags = {
    "management:product" = "4shells"
    "Name" = "four_shells_lb"
  }
  vpc_id = aws_vpc.four_shells.id
}

resource "aws_security_group" "four_shells_ecs" {
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    security_groups = [aws_security_group.four_shells_lb.id]
  }
  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  name = "four_shells_ecs"
  tags = {
    "management:product" = "4shells"
    "Name" = "four_shells_ecs"
  }
  vpc_id = aws_vpc.four_shells.id
}

resource "aws_subnet" "public_a" {
  availability_zone = "${var.region}a"
  cidr_block = "192.168.0.0/24"
  tags = {
    "management:product" = "4shells"
    "Name" = "public_a"
  }
  vpc_id = aws_vpc.four_shells.id
}

resource "aws_subnet" "public_b" {
  availability_zone = "${var.region}b"
  cidr_block = "192.168.1.0/24"
  tags = {
    "management:product" = "4shells"
    "Name" = "public_b"
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
    "management:product" = "4shells"
    "Name" = "4shells"
  }
}

terraform {
  backend "s3" {
    bucket = "4shells-infra-states"
    encrypt = true
    key = "infra.tfstate"
    region = "us-east-1"
  }
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "3.15.0"
    }
  }
  required_version = "0.13.5"
}

variable "access_key" {}

variable "region" {
  default = "us-east-1"
}

variable "secret_key" {}
