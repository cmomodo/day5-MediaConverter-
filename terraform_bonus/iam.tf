# Data source to get the current AWS account ID
data "aws_caller_identity" "current" {}

# IAM policy document for ECS task trust relationship
data "aws_iam_policy_document" "ecs_task_trust" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

#IAM role for ecs task execution
resource "aws_iam_role" "ecs_task_execution" {
  name               = "${var.project_name}-ecs-task-execution-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_trust.json
}

#attaach policy to ecs task execution role
resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
  role       = aws_iam_role.ecs_task_execution.name
}


# IAM policy document for custom IAM policy (example)
data "aws_iam_policy_document" "custom_policy" {
  statement {
    actions   = ["s3:GetObject", "s3:PutObject"]
    effect = "Allow"
    resources = [
      "arn:aws:s3:::${var.bucket_name}",
      "arn:aws:s3:::${var.bucket_name}/*"
    ]
  }

  # SSM Parameter Store Permissions
statement {
  actions = [
    "ssm:GetParameter",
    "ssm:GetParameters",
    "ssm:GetParameterHistory",
  ]
  effect = "Allow"
  resources = [
    "arn:aws:ssm:${var.region}:${data.aws_caller_identity.current.account_id}:parameter/highlight-pipeline-final/*",
    "arn:aws:ssm:${var.region}:${data.aws_caller_identity.current.account_id}:parameter/NCAHighlightsBackup/*",
  ]
}

#MediaConvert Permissions
statement {
  actions = [
    "mediaconvert:CreateJob*",
    "mediaconvert:ListJobs",
    "mediaconvert:GetJob",
  ]
  effect = "Allow"
  resources = ["*"]
}
}



#IAM policy for custom IAM policy
resource "aws_iam_policy" "custom_policy" {
  name        = "${var.project_name}-ecs-custom-policy"
  description = "Custom IAM policy for the project"
  policy      = data.aws_iam_policy_document.ecs_custom_policy.json
}

#attach the customer iam policy to the ecs task execution role
resource "aws_iam_role_policy_attachment" "custom_policy_attachment" {
  policy_arn = aws_iam_policy.custom_policy.arn
  role       = aws_iam_role.ecs_task_execution.name
}

#define the trust relationship for mediaconvert
data "aws_iam_policy_document" "mediaconvert_trust" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["mediaconvert.amazonaws.com"]
    }
  }
}

#create the mediaconvert role
resource "aws_iam_role" "mediaconvert_role" {
  name               = "${var.project_name}-mediaconvert-role"
  assume_role_policy = data.aws_iam_policy_document.mediaconvert_trust.json
}

#define media convert policy convert document.
data "aws_iam_policy_document" "mediaconvert_policy" {
  statement {
    actions = [
      "s3:GetObject",
      "s3:PutObject"
    ]
    effect = "Allow"
    resources = [
      "arn:aws:s3:::${var.bucket_name}",
    ]
  }

  statement {
    actions = [
      "logs:CreateLogGroup", # Added CreateLogGroup
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    effect    = "Allow"
    resources = [
      "arn:aws:logs:${var.region}:${data.aws_caller_identity.current.account_id}:log-group:/ecs/${var.project_name}*",
    ]
  }
}

# Create the MediaConvert policy
resource "aws_iam_policy" "mediaconvert_policy" {
  name   = "${var.project_name}-mediaconvert-s3-logs"
  policy = data.aws_iam_policy_document.mediaconvert_policy_doc.json
}

# Attach the MediaConvert policy to the MediaConvert role
resource "aws_iam_role_policy_attachment" "mediaconvert_attach" {
  role       = aws_iam_role.mediaconvert_role.name
  policy_arn = aws_iam_policy.mediaconvert_policy.arn
}