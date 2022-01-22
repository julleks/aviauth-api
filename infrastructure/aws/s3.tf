resource "aws_s3_bucket" "docs_bucket" {
  for_each = var.environments

  bucket = each.value.docs_domain_name

  policy = templatefile(
    "policies/s3-bucket-policy.tpl",
    {
      bucket_name = each.value.docs_domain_name,
      origin_access_identity = aws_cloudfront_origin_access_identity.docs_cloudfront_identity.id
    }
  )
}

resource "aws_s3_bucket" "www_docs_bucket" {
  for_each = var.environments

  bucket = "www.${each.value.docs_domain_name}"

  website {
    redirect_all_requests_to = "https://${each.value.docs_domain_name}"
  }
}

resource "aws_s3_bucket" "logs_bucket" {
  bucket = "${var.project_name}-logs"

  policy = templatefile(
    "policies/s3-bucket-policy-logs.tpl",
    {
      bucket_name = "${var.project_name}-logs",
      account_id = var.account_id
    }
  )
}
