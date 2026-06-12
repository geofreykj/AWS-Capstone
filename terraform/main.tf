########################################
# ECR
########################################

resource "aws_ecr_repository" "rag_app" {
  name = "rag-capstone"
}

########################################
# Default VPC
########################################

locals {
  subnet_ids = [
    "subnet-071617bf3783c05da",
    "subnet-0db32eba5916952f6"
  ]

  vpc_id = "vpc-0330b61a7e3afeb82"
}

########################################
# ECS Cluster
########################################

resource "aws_ecs_cluster" "rag_cluster" {
  name = "rag-cluster"
}

########################################
# Security Group
########################################

resource "aws_security_group" "ecs_sg" {
  name        = "rag-ecs-sg"
  description = "Allow Streamlit"
  vpc_id      = local.vpc_id

  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

########################################
# ECS Task Execution Role
########################################

resource "aws_iam_role" "ecs_execution_role" {
  name = "rag-ecs-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_execution_role_policy" {
  role       = aws_iam_role.ecs_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

########################################
# ECS Task Role
########################################

resource "aws_iam_role" "ecs_task_role" {
  name = "rag-ecs-task-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "bedrock_s3_policy" {
  name = "bedrock-s3-policy"
  role = aws_iam_role.ecs_task_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = "*"
      }
    ]
  })
}

########################################
# CloudWatch Logs
########################################

resource "aws_cloudwatch_log_group" "ecs_logs" {
  name              = "/ecs/rag-capstone"
  retention_in_days = 7
}

########################################
# ECS Task Definition
########################################

resource "aws_ecs_task_definition" "rag_task" {
  family                   = "rag-capstone"
  requires_compatibilities = ["FARGATE"]

  network_mode = "awsvpc"

  cpu    = "1024"
  memory = "2048"

  execution_role_arn = aws_iam_role.ecs_execution_role.arn
  task_role_arn      = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name  = "rag-container"

      image = "092040680312.dkr.ecr.us-east-1.amazonaws.com/rag-capstone:latest"

      essential = true

      portMappings = [
        {
          containerPort = 8501
          hostPort      = 8501
          protocol      = "tcp"
        }
      ]

      environment = [
        {
          name  = "AWS_REGION"
          value = "us-east-1"
        },
        {
          name  = "BUCKET_NAME"
          value = "rag-capstone-jeff"
        },
        {
          name  = "MODEL_ID"
          value = "amazon.nova-lite-v1:0"
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"

        options = {
          awslogs-group         = aws_cloudwatch_log_group.ecs_logs.name
          awslogs-region        = "us-east-1"
          awslogs-stream-prefix = "ecs"
        }
      }
    }
  ])
}

########################################
# ECS Service
########################################

resource "aws_ecs_service" "rag_service" {
  name            = "rag-service"
  cluster         = aws_ecs_cluster.rag_cluster.id
  task_definition = aws_ecs_task_definition.rag_task.arn

  desired_count = 1
  launch_type   = "FARGATE"

  network_configuration {
    assign_public_ip = true

    security_groups = [
      aws_security_group.ecs_sg.id
    ]

    subnets = local.subnet_ids
  }
}