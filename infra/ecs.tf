resource "aws_ecs_cluster" "four_shells" {
  name = "4shells"
  tags = {
    "Name" = "4shells"
    "management:product" = "4shells"
  }
}
