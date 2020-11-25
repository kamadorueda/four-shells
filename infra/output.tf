output "four_shells_lb_dns" {
  value = aws_lb.four_shells.dns_name
}

output "AWS_ACCESS_KEY_ID_ADMIN" {
  value = aws_iam_access_key.admin.id
}

output "AWS_ACCESS_KEY_ID_SERVER" {
  value = aws_iam_access_key.server.id
}

output "AWS_CLOUDFRONT_DOMAIN" {
  value = aws_cloudfront_distribution.four_shells_public_content.domain_name
}

output "AWS_SECRET_ACCESS_KEY_ADMIN" {
  value = aws_iam_access_key.admin.secret
}

output "AWS_SECRET_ACCESS_KEY_SERVER" {
  value = aws_iam_access_key.server.secret
}
