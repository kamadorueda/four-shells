config {
  deep_check = true
  module = true
}

rule "aws_resource_missing_tags" {
  enabled = true
  tags = [
    "Name",
    "management:product",
  ]
}
