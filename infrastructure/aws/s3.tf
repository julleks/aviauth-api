resource "aws_s3_bucket" "docs-bucket" {
  bucket = var.docs_domain_name

  policy = templatefile(
    "policies/s3-policy.tpl",
    {
      bucket_name = var.docs_domain_name,
      origin_access_identity = aws_cloudfront_origin_access_identity.docs-cloudfront-identity.id
    }
  )
}

resource "aws_s3_bucket" "www-docs-bucket" {
  bucket = "www.${var.docs_domain_name}"

  website {
    redirect_all_requests_to = "https://${var.docs_domain_name}"
  }
}

resource "aws_s3_bucket" "logs-docs-bucket" {
  bucket = "logs.${var.docs_domain_name}"

  grant {
    id = "c4c1ede66af53448b93c283ce9448c4ba468c9432aa01d700d3878632f77d2d0"
    permissions = [
      "FULL_CONTROL",
    ]
    type = "CanonicalUser"
  }

   grant {
     id = "cd5e47cd9cc9eab5006df82580fa1614dcbd0e5c19163c241d31d27f42082271"
     permissions = [
       "FULL_CONTROL",
     ]
     type = "CanonicalUser"
  }

  grant {
    permissions = [
      "READ_ACP",
      "WRITE",
    ]
    type = "Group"
    uri = "http://acs.amazonaws.com/groups/s3/LogDelivery"
  }
}
