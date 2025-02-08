resource "aws_ecr_repository" "my_repository" {
  name = "${var.project_name}-repository"
}
