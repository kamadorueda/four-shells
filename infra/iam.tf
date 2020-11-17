data "aws_iam_policy_document" "admin" {
  statement {
    effect  = "Allow"
    actions = [
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

resource "aws_iam_access_key" "admin" {
  user = aws_iam_user.admin.name
  status = "Active"
}

resource "aws_iam_policy" "admin" {
  name = "admin"
  policy = data.aws_iam_policy_document.admin.json
}

resource "aws_iam_user" "admin" {
  name = "admin"
  tags = {
    "Name" = "admin"
    "management:product" = "common"
  }
}

resource "aws_iam_user_policy_attachment" "admin" {
  user = "admin"
  policy_arn = aws_iam_policy.admin.arn
}
