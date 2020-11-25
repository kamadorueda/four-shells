data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "admin" {
  statement {
    effect = "Allow"
    actions = [
      "autoscaling:*",
      "cloudfront:*",
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

data "aws_iam_policy_document" "server" {
  statement {
    effect = "Allow"
    actions = [
      "dynamodb:*",
    ]
    resources = ["*"]
  }
}

data "aws_iam_policy_document" "four_shells_public_content" {
  statement {
    actions = ["s3:GetObject"]
    effect  = "Allow"
    principals {
      identifiers = [
        aws_cloudfront_origin_access_identity.four_shells_public_content.iam_arn
      ]
      type = "AWS"
    }
    resources = ["${aws_s3_bucket.four_shells_public_content.arn}/*"]
  }
}
