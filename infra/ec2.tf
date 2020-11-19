resource "aws_autoscaling_group" "four_shells" {
  desired_capacity = 0
  health_check_type = "EC2"
  launch_configuration = aws_launch_configuration.four_shells.name
  max_size = 1
  min_size = 0
  name = "4shells"
  tags = [
    {
      key = "Name"
      propagate_at_launch = false
      value = "4shells"
    },
    {
      key = "management:product"
      propagate_at_launch = false
      value = "4shells"
    },
  ]
  vpc_zone_identifier = [
    aws_subnet.public_1.id,
  ]
}

resource "aws_launch_configuration" "four_shells" {
  associate_public_ip_address = true
  iam_instance_profile = aws_iam_instance_profile.ecs.name
  image_id = "ami-059628695ae4c249b"
  instance_type = "t2.micro"
  name = "4shells"
  security_groups = [
    aws_security_group.four_shells_ecs.id,
  ]
  user_data = file("${path.module}/ecs_user_data.sh")
}
