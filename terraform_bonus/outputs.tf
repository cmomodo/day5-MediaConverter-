# bucket
resource "aws_s3_bucket" "my_bucket" {
  bucket = var.bucket_name
  
}

#output for ecr repostory
output "ecr_repository_url" {
  value = aws_ecr_repository.my_repository.repository_url
}

#output for ecs cluster
output "ecs_cluster_name" {
  value = aws_ecs_cluster.my_cluster.name
}

#output for ecs service name 
output "ecs_service_name" {
  value = aws_ecs_service.my_service.name
}

#output for media convert role arn 
output "mediaconvert_role_arn" {
  value = aws_iam_role.mediaconvert_role.arn
}