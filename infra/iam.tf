data "aws_iam_policy_document" "admin" {
  statement {
    effect = "Allow"
    actions = [
      "autoscaling:*",
      "dynamodb:*",
      "ec2:*",
      "ecr:*",
      "ecs:*",
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
