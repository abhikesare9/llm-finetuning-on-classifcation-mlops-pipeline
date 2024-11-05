variable "region" {
  type        = string
  default     = "us-west-1"
  description = "Default region to provision the infrastructure"
}
variable "cidr_block" {
  type        = string
  default     = "10.168.0.0/16"
  description = "vpc cidr block"
}

variable "public_subnet_cidrs" {
  type        = list(string)
  default     = ["10.168.192.0/19", "10.168.224.0/19"]
  description = "public subnet cidr blocks for vpc"
}

variable "private_subnet_cidrs" {
  type        = list(string)
  default     = ["10.168.0.0/18", "10.168.64.0/18", "10.168.128.0/18"]
  description = "private subnet cidr blocks for vpc."
}


variable "azs" {
  type        = list(string)
  description = "Availability Zones"
  default     = ["us-west-1a", "us-west-1b", "us-west-1c"]
}


variable bucket_name {
  type        = string
  default     = "devops-infra-backup-terraform"
  description = "terraform backend s3 bucket"
}

variable profile {
  type        = string
  default     = "dev"
  description = "aws profile for creation"
}