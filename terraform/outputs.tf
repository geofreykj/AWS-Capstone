output "cluster_name" {
  value = aws_ecs_cluster.rag_cluster.name
}

output "ecr_repo_url" {
  value = aws_ecr_repository.rag_app.repository_url
}