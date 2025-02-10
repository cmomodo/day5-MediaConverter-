terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

locals {
  container_definitions = file("./container_definitions.fpl")
}

# Configure the AWS Provider
provider "aws" {
  region = var.region
}


