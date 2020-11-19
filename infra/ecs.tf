resource "aws_ecs_cluster" "four_shells" {
  name = "4shells"
  tags = {
    "management:product" = "4shells"
    "Name" = "4shells"
  }
}

resource "aws_ecs_task_definition" "four_shells" {
  container_definitions = jsonencode([
    {
      command = [
        "echo"
      ]
      cpu = 1
      environment = [
      ]
      essential = true
      image = "docker.pkg.github.com/kamadorueda/4shells.com/4shells.com:latest"
      links = []
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group = aws_cloudwatch_log_group.four_shells.name
          awslogs-region = var.region
          awslogs-stream-prefix = aws_cloudwatch_log_stream.four_shells.name
        }
      }
      memory = 900
      name = "4shells"
      portMappings = [
        {
          containerPort = 8000
          hostPort = 0
          protocol = "tcp"
        }
      ]
    },
  ])
  family = "4shells"
  tags = {
    "management:product" = "4shells"
    "Name" = "4shells"
  }
}
