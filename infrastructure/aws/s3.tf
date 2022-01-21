resource "aws_s3_bucket" "docs-bucket" {
  for_each = var.environments

  bucket = each.value.docs_domain_name

  policy = templatefile(
    "policies/s3-bucket-policy.tpl",
    {
      bucket_name = each.value.docs_domain_name,
      origin_access_identity = aws_cloudfront_origin_access_identity.docs-cloudfront-identity.id
    }
  )
}

resource "aws_s3_bucket" "www-docs-bucket" {
  for_each = var.environments

  bucket = "www.${each.value.docs_domain_name}"

  website {
    redirect_all_requests_to = "https://${each.value.docs_domain_name}"
  }
}

resource "aws_s3_bucket" "logs-docs-bucket" {
  for_each = var.environments

  bucket = "logs.${each.value.docs_domain_name}"

  policy = templatefile(
    "policies/s3-bucket-policy-logs.tpl",
    {
      bucket_name = "logs.${each.value.docs_domain_name}",
      bucket_logging_prefix = each.value.cloudfront-logs-prefix-docs,
      account_id = var.account_id
    }
  )
}
