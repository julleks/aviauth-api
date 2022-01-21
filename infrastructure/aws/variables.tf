variable "region" {
  default = "eu-west-1"
}

variable "domain_name" {}

variable "environments" {
  type = map(object({
    docs_domain_name = string
  }))
}
