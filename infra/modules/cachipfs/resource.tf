# Tables structure:
#
# table_name:
#  hash_key, range_key:
#    - attr: attr_value
#
# accounts:
#  email:
#    balance: integer
#    namespaces: [id1, id2, ...]
#
# namespaces:
#  id:
#    name: ns_name
#    tokens: [id1, id2, ...]
#
# objects:
#  ns, key:
#    value: value
#    ...

resource "aws_dynamodb_table" "cachipfs_accounts" {
  attribute {
    name = "email"
    type = "S"
  }
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "email"
  name         = "cachipfs_accounts"
  tags = {
    "management:product" = "cachipfs"
    "Name"               = "cachipfs_accounts"
  }
}

resource "aws_dynamodb_table" "cachipfs_namespaces" {
  attribute {
    name = "id"
    type = "S"
  }
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"
  name         = "cachipfs_namespaces"
  tags = {
    "management:product" = "cachipfs"
    "Name"               = "cachipfs_namespaces"
  }
}

resource "aws_dynamodb_table" "cachipfs_objects" {
  attribute {
    name = "ns"
    type = "S"
  }
  attribute {
    name = "key"
    type = "S"
  }
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "ns"
  name         = "cachipfs_objects"
  range_key    = "key"
  tags = {
    "management:product" = "cachipfs"
    "Name"               = "cachipfs_objects"
  }
  ttl {
    attribute_name = "ttl"
    enabled        = true
  }
}
