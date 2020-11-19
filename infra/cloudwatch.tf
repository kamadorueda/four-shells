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
