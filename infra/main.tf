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

data "aws_iam_policy_document" "four_shells_ecs" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      identifiers = [
        "ecs.amazonaws.com",
        "ec2.amazonaws.com",
      ]
      type = "Service"
    }
  }
}

data "aws_iam_policy_document" "four_shells_ecs_service" {
  statement {
    actions = [
      "ec2:*",
      "elasticloadbalancing:*",
    ]
    effect    = "Allow"
    resources = ["*"]
  }
}

output "admin_key" {
  sensitive = true
  value     = aws_iam_access_key.admin.id
}

output "admin_secret" {
  sensitive = true
  value     = aws_iam_access_key.admin.secret
}

provider "aws" {
  access_key = var.access_key
  secret_key = var.secret_key
  region     = var.region
}

resource "aws_autoscaling_group" "four_shells" {
  desired_capacity          = var.replicas
  health_check_grace_period = 300
  health_check_type         = "EC2"
  launch_configuration      = aws_launch_configuration.four_shells.name
  lifecycle {
    create_before_destroy = true
  }
  max_size = var.replicas
  min_size = var.replicas
  name     = "four_shells"
  tags = [
    {
      key                 = "Name"
      propagate_at_launch = true
      value               = "four_shells"
    },
    {
      key                 = "management:product"
      propagate_at_launch = true
      value               = "four_shells"
    },
  ]
  vpc_zone_identifier = [
    aws_subnet.four_shells_public_a.id,
    aws_subnet.four_shells_public_b.id,
  ]
}

resource "aws_cloudwatch_log_group" "four_shells" {
  name              = "/ecs/four_shells"
  retention_in_days = 1
  tags = {
    "management:product" = "four_shells"
    "Name"               = "four_shells"
  }
}

resource "aws_cloudwatch_log_stream" "four_shells" {
  log_group_name = aws_cloudwatch_log_group.four_shells.name
  name           = "four_shells"
}

resource "aws_ecr_repository" "four_shells" {
  name = "four_shells"
  tags = {
    "Name"               = "four_shells"
    "management:product" = "four_shells"
  }
}

resource "aws_ecr_lifecycle_policy" "four_shells" {
  repository = aws_ecr_repository.four_shells.name

  policy = jsonencode({
    rules = [
      {
        action = {
          type = "expire"
        }
        rulePriority = 1
        selection = {
          countType   = "imageCountMoreThan",
          countNumber = 1,
          tagStatus   = "untagged"
        }
      },
    ],
  })
}

resource "aws_ecs_cluster" "four_shells" {
  name = "four_shells"
  tags = {
    "management:product" = "four_shells"
    "Name"               = "four_shells"
  }
}

resource "aws_ecs_service" "four_shells" {
  cluster = aws_ecs_cluster.four_shells.id
  depends_on = [
    aws_lb_listener.four_shells,
    aws_iam_role_policy.four_shells_ecs_service,
  ]
  desired_count = var.replicas
  // force_new_deployment = true
  iam_role = aws_iam_role.four_shells_ecs_service.arn
  load_balancer {
    target_group_arn = aws_lb_target_group.four_shells.arn
    container_name   = "four_shells"
    container_port   = 8400
  }
  name = "four_shells"
  tags = {
    "management:product" = "four_shells"
    "Name"               = "four_shells"
  }
  task_definition = aws_ecs_task_definition.four_shells.arn
}

resource "aws_ecs_task_definition" "four_shells" {
  container_definitions = jsonencode([
    {
      command     = ["4shells"]
      cpu         = 1
      environment = []
      essential   = true
      image       = "791877604510.dkr.ecr.us-east-1.amazonaws.com/four_shells:latest"
      memory      = 900
      name        = "four_shells"
      portMappings = [
        {
          containerPort = 8400
          hostPort      = 0
          protocol      = "tcp"
        },
      ]
    },
  ])
  family = "four_shells"
  tags = {
    "management:product" = "four_shells"
    "Name"               = "four_shells"
  }
}

resource "aws_iam_access_key" "admin" {
  user   = aws_iam_user.admin.name
  status = "Active"
}

resource "aws_iam_instance_profile" "four_shells_ecs" {
  name = "four_shells_ecs"
  role = aws_iam_role.four_shells_ecs.name
}

resource "aws_iam_policy" "admin" {
  name   = "admin"
  policy = data.aws_iam_policy_document.admin.json
}

resource "aws_iam_role" "four_shells_ecs" {
  assume_role_policy = data.aws_iam_policy_document.four_shells_ecs.json
  name               = "four_shells_ecs"
  tags = {
    "management:product" = "four_shells"
    "Name"               = "four_shells_ecs"
  }
}

resource "aws_iam_role" "four_shells_ecs_service" {
  assume_role_policy = data.aws_iam_policy_document.four_shells_ecs.json
  name               = "four_shells_ecs_service"
  tags = {
    "management:product" = "four_shells"
    "Name"               = "four_shells_ecs_service"
  }
}

resource "aws_iam_role_policy" "four_shells_ecs_service" {
  name   = "ecs_service_role_policy"
  policy = data.aws_iam_policy_document.four_shells_ecs_service.json
  role   = aws_iam_role.four_shells_ecs_service.id
}

resource "aws_iam_role_policy_attachment" "four_shells_ecs" {
  role       = aws_iam_role.four_shells_ecs.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

resource "aws_iam_user" "admin" {
  name = "admin"
  tags = {
    "management:product" = "four_shells"
    "Name"               = "admin"
  }
}

resource "aws_iam_user_policy_attachment" "admin" {
  user       = "admin"
  policy_arn = aws_iam_policy.admin.arn
}

resource "aws_internet_gateway" "four_shells" {
  tags = {
    "management:product" = "four_shells"
    "Name"               = "four_shells"
  }
  vpc_id = aws_vpc.four_shells.id
}

resource "aws_key_pair" "four_shells" {
  key_name   = "four_shells"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC2vjw0Q8yT4TJWSfdkcgm2FPaIwetGNo9FmHG2I/xXP+EB3GddUMbhHA4v9w8jvsbuxEmkYiMPwOO/1q/8dFjuUaRR22y3N0hNFGxPDvQeUuZFl7HH4kZ60Yki0uHiCgbJds+qmDZvpYeiZsGuOYO/AaQjMcMduEcKoLpzIOZiM3bWSkotblJTaukSf/9zUvGAsYL//S/uE4DANnKg1p9XNNFLOCcDoxJpGR9oT6c+lsw9rJpkXSSES6+72WPctN5GCRdujXytF30CY040bO16dflzG8YDhb/QK6MdqEKHL12mN0ijWnfJa9e8AsQ9I3WudmFavxgk6J/uWHTWCxyt"
  tags = {
    "management:product" = "four_shells"
    "Name"               = "four_shells"
  }
}

resource "aws_launch_configuration" "four_shells" {
  associate_public_ip_address = true
  iam_instance_profile        = aws_iam_instance_profile.four_shells_ecs.name
  image_id                    = "ami-0f161e6034a6262d8"
  instance_type               = "t2.micro"
  key_name                    = aws_key_pair.four_shells.key_name
  lifecycle {
    create_before_destroy = true
  }
  name_prefix = "four_shells_"
  security_groups = [
    aws_security_group.four_shells_ecs.id,
  ]
  user_data = "#!/bin/bash\necho ECS_CLUSTER=${aws_ecs_cluster.four_shells.name} >> /etc/ecs/ecs.config"
}

resource "aws_lb" "four_shells" {
  # https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb
  internal           = false
  load_balancer_type = "application"
  name               = "four-shells"
  security_groups = [
    aws_security_group.four_shells_lb.id,
  ]
  subnets = [
    aws_subnet.four_shells_public_a.id,
    aws_subnet.four_shells_public_b.id,
  ]
  tags = {
    "management:product" = "four_shells"
    "Name"               = "four_shells"
  }
}

resource "aws_lb_listener" "four_shells" {
  # https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb_listener
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.four_shells.arn
  }
  depends_on = [
    aws_lb_target_group.four_shells,
  ]
  load_balancer_arn = aws_lb.four_shells.id
  port              = "80"
  protocol          = "HTTP"
}

resource "aws_lb_target_group" "four_shells" {
  # https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb_target_group
  health_check {
    path    = "/ping"
    matcher = "200"
  }
  name     = "four-shells"
  port     = 80
  protocol = "HTTP"
  tags = {
    "management:product" = "four_shells"
    "Name"               = "four_shells"
  }
  vpc_id = aws_vpc.four_shells.id
}

resource "aws_route_table" "four_shells_public" {
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.four_shells.id
  }
  tags = {
    "management:product" = "four_shells"
    "Name"               = "public"
  }
  vpc_id = aws_vpc.four_shells.id
}

resource "aws_route_table_association" "four_shells_public_a" {
  route_table_id = aws_route_table.four_shells_public.id
  subnet_id      = aws_subnet.four_shells_public_a.id
}

resource "aws_route_table_association" "four_shells_public_b" {
  route_table_id = aws_route_table.four_shells_public.id
  subnet_id      = aws_subnet.four_shells_public_b.id
}

resource "aws_security_group" "four_shells_ecs" {
  egress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 0
    protocol    = "-1"
    to_port     = 0
  }
  ingress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 0
    protocol    = "-1"
    to_port     = 0
  }
  name = "four_shells_ecs"
  tags = {
    "management:product" = "four_shells"
    "Name"               = "four_shells_ecs"
  }
  vpc_id = aws_vpc.four_shells.id
}

resource "aws_security_group" "four_shells_lb" {
  egress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 0
    protocol    = "-1"
    to_port     = 0
  }
  ingress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 80
    protocol    = "tcp"
    to_port     = 80
  }
  ingress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 443
    protocol    = "tcp"
    to_port     = 443
  }
  name = "four_shells_lb"
  tags = {
    "management:product" = "four_shells"
    "Name"               = "four_shells_lb"
  }
  vpc_id = aws_vpc.four_shells.id
}

resource "aws_subnet" "four_shells_public_a" {
  availability_zone = "${var.region}a"
  cidr_block        = "10.0.0.0/18"
  tags = {
    "management:product" = "four_shells"
    "Name"               = "four_shells_public_a"
  }
  vpc_id = aws_vpc.four_shells.id
}

resource "aws_subnet" "four_shells_public_b" {
  availability_zone = "${var.region}b"
  cidr_block        = "10.0.64.0/18"
  tags = {
    "management:product" = "four_shells"
    "Name"               = "four_shells_public_b"
  }
  vpc_id = aws_vpc.four_shells.id
}

resource "aws_vpc" "four_shells" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = {
    "management:product" = "four_shells"
    "Name"               = "four_shells"
  }
}

terraform {
  backend "s3" {
    bucket  = "four_shells-infra-states"
    encrypt = true
    key     = "infra.tfstate"
    region  = "us-east-1"
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.15.0"
    }
  }
  required_version = "0.13.5"
}

variable "access_key" {}

variable "replicas" {
  default = 1
}

variable "region" {
  default = "us-east-1"
}

variable "secret_key" {}

# Attempts
