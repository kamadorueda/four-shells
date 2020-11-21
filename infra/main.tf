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

output "four_shells_lb_dns" {
  value = aws_lb.four_shells.dns_name
}

provider "acme" {
  server_url = "https://acme-v02.api.letsencrypt.org/directory"
}

provider "aws" {
  access_key = var.aws_access_key_id
  secret_key = var.aws_secret_access_key
  region     = var.region
}

provider "tls" {}

resource "acme_certificate" "four_shells" {
  account_key_pem         = acme_registration.four_shells.account_key_pem
  certificate_request_pem = tls_cert_request.four_shells.cert_request_pem

  dns_challenge {
    provider = "cloudflare"
    config = {
      CF_DNS_API_TOKEN = var.cf_dns_api_token
    }
  }
}

resource "acme_registration" "four_shells" {
  account_key_pem = tls_private_key.four_shells_registry.private_key_pem
  email_address   = var.acme_email_address
}

resource "aws_autoscaling_group" "four_shells" {
  # https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/autoscaling_group
  desired_capacity          = var.service_replicas
  health_check_grace_period = 300
  health_check_type         = "EC2"
  launch_configuration      = aws_launch_configuration.four_shells.name
  lifecycle {
    create_before_destroy = true
  }
  max_instance_lifetime = 604800
  max_size              = 2 * var.service_replicas
  min_size              = var.service_replicas
  name                  = "four_shells"
  protect_from_scale_in = true
  tags = [
    {
      key                 = "AmazonECSManaged"
      propagate_at_launch = true
      value               = ""
    },
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
  # https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group
  name              = "/four_shells"
  retention_in_days = 1
  tags = {
    "management:product" = "four_shells"
    "Name"               = "four_shells"
  }
}

resource "aws_cloudwatch_log_stream" "four_shells" {
  # https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_stream
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

resource "aws_ecs_capacity_provider" "four_shells" {
  # https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecs_capacity_provider
  auto_scaling_group_provider {
    auto_scaling_group_arn = aws_autoscaling_group.four_shells.arn
    managed_scaling {
      maximum_scaling_step_size = 1
      minimum_scaling_step_size = 1
      status                    = "ENABLED"
      target_capacity           = var.service_replicas
    }
    managed_termination_protection = "ENABLED"
  }
  name = "four_shells"
  tags = {
    "management:product" = "four_shells"
    "Name"               = "four_shells"
  }
}

resource "aws_ecs_cluster" "four_shells" {
  # https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecs_cluster
  capacity_providers = [
    aws_ecs_capacity_provider.four_shells.name,
  ]
  default_capacity_provider_strategy {
    capacity_provider = aws_ecs_capacity_provider.four_shells.name
  }
  name = var.aws_ecs_cluster_name
  tags = {
    "management:product" = "four_shells"
    "Name"               = "four_shells"
  }
}

resource "aws_ecs_service" "four_shells" {
  # https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecs_service
  cluster = aws_ecs_cluster.four_shells.id
  depends_on = [
    aws_lb_listener.four_shells_http,
    aws_lb_listener.four_shells_https,
    aws_iam_role_policy.four_shells_ecs_service,
  ]
  desired_count        = var.service_replicas
  force_new_deployment = var.service_deploy_on_each_apply
  iam_role             = aws_iam_role.four_shells_ecs_service.arn
  lifecycle {
    ignore_changes = [
      desired_count,
    ]
  }
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
  # https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecs_task_definition
  container_definitions = jsonencode([
    {
      command     = ["4shells"]
      cpu         = 1
      environment = []
      essential   = true
      image       = "791877604510.dkr.ecr.us-east-1.amazonaws.com/four_shells:latest"
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_stream.four_shells.log_group_name
          awslogs-region        = var.region
          awslogs-stream-prefix = aws_cloudwatch_log_stream.four_shells.name
        }
      }
      memory = 900
      name   = "four_shells"
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

resource "aws_iam_server_certificate" "four_shells" {
  name_prefix      = "four_shells_"
  certificate_body = acme_certificate.four_shells.certificate_pem
  private_key      = tls_private_key.four_shells_certificate.private_key_pem

  lifecycle {
    create_before_destroy = true
  }
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
  user_data = "#!/bin/bash\necho ECS_CLUSTER=${var.aws_ecs_cluster_name} >> /etc/ecs/ecs.config"
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

resource "aws_lb_listener" "four_shells_http" {
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

resource "aws_lb_listener" "four_shells_https" {
  # https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb_listener
  certificate_arn = aws_iam_server_certificate.four_shells.arn
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.four_shells.arn
  }
  depends_on = [
    aws_lb_target_group.four_shells,
  ]
  load_balancer_arn = aws_lb.four_shells.id
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
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

resource "tls_cert_request" "four_shells" {
  key_algorithm   = "RSA"
  private_key_pem = tls_private_key.four_shells_certificate.private_key_pem
  subject {
    common_name  = "*.4shells.com"
    organization = "Four Shells"
  }
}

resource "tls_private_key" "four_shells_certificate" {
  algorithm = "RSA"
}

resource "tls_private_key" "four_shells_registry" {
  algorithm = "RSA"
}

terraform {
  backend "s3" {
    bucket  = "4shells-infra-states"
    encrypt = true
    key     = "infra.tfstate"
    region  = "us-east-1"
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.15.0"
    }
    acme = {
      source  = "terraform-providers/acme"
      version = "1.5.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "3.0.0"
    }
  }
  required_version = "0.13.5"
}

variable "acme_email_address" {}

variable "aws_access_key_id" {}

variable "aws_ecs_cluster_name" {
  default = "four_shells"
}

variable "aws_secret_access_key" {}

variable "cf_dns_api_token" {}

variable "region" {
  default = "us-east-1"
}

variable "service_deploy_on_each_apply" {
  default = false
}

variable "service_replicas" {
  default = 1
}
