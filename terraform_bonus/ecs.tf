resource "aws_ecs_cluster" "my_cluster" {
  name = "${var.project_name}-cluster"
}

#cloudwatch and ecs log group
resource "aws_cloudwatch_log_group" "my_cluster" {
  name              = "ecs/${var.project_name}-ecs-log-group"
  retention_in_days = 7
}

# Create ECS Task Definition
resource "aws_ecs_task_definition" "my_cluster" {
  family                   = "${var.project_name}-task"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn

  container_definitions = jsonencode([
    {
      name      = "${var.project_name}-container"
      image     = "${aws_ecr_repository.my_repository.repository_url}:latest"
      essential = true

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/${var.project_name}"
          "awslogs-region"        = var.region
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])
}

#ecs service
resource "aws_ecs_service" "my_service" { # Keeping this as my_service to match your outputs.tf
  name            = "${var.project_name}-service"
  cluster         = aws_ecs_cluster.my_cluster.id          # Updated reference
  task_definition = aws_ecs_task_definition.my_cluster.arn # Updated reference
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.public_subnets
    security_groups  = [aws_security_group.ecs_task.id]
    assign_public_ip = true
  }

  deployment_controller {
    type = "ECS"
  }

  tags = {
    Name = "${var.project_name}-service"
  }
}
