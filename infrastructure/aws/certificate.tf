resource "aws_acm_certificate" "certificate" {
  provider = aws.acm_provider
  domain_name = "*.${var.domain_name}"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_acm_certificate_validation" "certificate-validation" {
  provider = aws.acm_provider
  certificate_arn         = aws_acm_certificate.certificate.arn
  validation_record_fqdns = [for record in aws_route53_record.certificate-cname-record : record.fqdn]
}
