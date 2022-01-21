variable "region" {
  default = "eu-west-1"
}

variable "account_id" {}

variable "domain_name" {}

variable "environments" {
  type = map(object({
    docs_domain_name = string
    cloudfront-logs-prefix-docs = string
  }))
}
