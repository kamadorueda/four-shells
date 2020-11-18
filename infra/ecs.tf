resource "aws_ecs_cluster" "four_shells" {
  name = "4shells"
  tags = {
    "management:product" = "4shells"
    "Name" = "4shells"
  }
}
