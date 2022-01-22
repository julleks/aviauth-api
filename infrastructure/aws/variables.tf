variable "region" {
  default = "eu-west-1"
}

variable "account_id" {}

variable "project_name" {}

variable "root_domain_name" {}

variable "environments" {
  type = map(object({
    docs_domain_name = string
  }))
}
