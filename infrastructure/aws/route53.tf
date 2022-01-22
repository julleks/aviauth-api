resource "aws_route53_zone" "primary" {
  name = var.root_domain_name
}

resource "aws_route53_record" "ns_record" {
  name = var.root_domain_name
  type = "NS"
  zone_id = aws_route53_zone.primary.zone_id
  records = [
    aws_route53_zone.primary.name_servers[0],
    aws_route53_zone.primary.name_servers[1],
    aws_route53_zone.primary.name_servers[2],
    aws_route53_zone.primary.name_servers[3],
  ]
  ttl = 172800
}

resource "aws_route53_record" "soa_record" {
  name = var.root_domain_name
  type = "SOA"
  zone_id = aws_route53_zone.primary.zone_id
  records = [
    "ns-1304.awsdns-35.org. awsdns-hostmaster.amazon.com. 1 7200 900 1209600 86400",
  ]
  ttl = 900
}

resource "aws_route53_record" "certificate_cname_record" {
  for_each = {
    for dvo in aws_acm_certificate.certificate.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name = each.value.name
  type = each.value.type
  zone_id = aws_route53_zone.primary.zone_id
  records = [
    each.value.record
  ]
  ttl = 60
}

resource "aws_route53_record" "docs_a_record" {
  for_each = var.environments

  name = each.value.docs_domain_name
  type = "A"
  zone_id = aws_route53_zone.primary.zone_id

  alias {
    evaluate_target_health = false
    name = aws_cloudfront_distribution.docs_cloudfront[each.key].domain_name
    zone_id = aws_cloudfront_distribution.docs_cloudfront[each.key].hosted_zone_id
  }
}

resource "aws_route53_record" "www_docs_a_record" {
  for_each = var.environments

  name = "www.${each.value.docs_domain_name}"
  type = "A"
  zone_id = aws_route53_zone.primary.zone_id

  alias {
    evaluate_target_health = false
    name = "s3-website-eu-west-1.amazonaws.com"
    zone_id = aws_s3_bucket.www_docs_bucket[each.key].hosted_zone_id
  }
}
