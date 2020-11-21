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
