resource "aws_cloudwatch_log_group" "four_shells" {
  name = "/ecs/4shells"
  retention_in_days = 1
}

resource "aws_cloudwatch_log_stream" "four_shells" {
  name = "4shells"
  log_group_name = aws_cloudwatch_log_group.four_shells.name
}
