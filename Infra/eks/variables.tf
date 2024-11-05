variable cluster_name {
  type        = string
  default     = "devops_infra"
  description = "eks cluster name"
}
variable region {
  type        = string
  default     = "us-east-1"
  description = "default eks region"
}


variable bucket_name {
  type        = string
  default     = "devops_infra_backup"
  description = "s3 backend configurations for eks"
}

variable controle_plane_iam_role {
  type        = string
  default     = "arn:aws:iam::730335570705:role/eksclustercontrolplanerole"
  description = "IAM role for control plane"
}

variable eks_version {
  type        = string
  default     = "1.25"
  description = "eks version to be deployed"
}

variable workernode_iam_role {
  type        = string
  default     = "arn:aws:iam::730335570705:role/workernoderole"
  description = "IAM role for worker nodes"
}

variable ssh_key_name {
  type        = string
  default     = "devops_infra"
  description = "ssh key for logging in to worker nodes"
}

variable workernode_instance_type {
  type        = string
  default     = "t2.micro"
  description = "description"
}

variable workernode_storage {
  type        = number
  default     = 30
  description = "disk allocated to worker nodes"
}

variable desired_size {
  type        = string
  default     = "3"
  description = "desired number of worker nodes"
}
variable maximum_worker_nodes {
  type        = string
  default     = "5"
  description = "maximum number of worker nodes"
}

variable min_worker_nodes {
  type        = string
  default     = "1"
  description = "min number of worker nodes"
}
variable profile {
  type        = string
  default     = "dev"
  description = "aws resource creation profile"
}