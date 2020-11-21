output "admin_key" {
  sensitive = true
  value     = aws_iam_access_key.admin.id
}

output "admin_secret" {
  sensitive = true
  value     = aws_iam_access_key.admin.secret
}

output "four_shells_lb_dns" {
  value = aws_lb.four_shells.dns_name
}
