resource "aws_security_group" "api_load_balancer_sg" {
  name        = "${var.base_name}-api-load-balancer"
  description = "Rules for access to the ${var.base_name} API load balancer"
  vpc_id      = var.vpc_id
  tags        = {}
}

resource "aws_security_group_rule" "api_public_access" {
  type              = "ingress"
  description       = "Inbound access to the API load balancer"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.api_load_balancer_sg.id
  ipv6_cidr_blocks  = []
  prefix_list_ids   = []
}

resource "aws_security_group_rule" "api_container_access" {
  type                     = "egress"
  description              = "Outbound access to API containers"
  from_port                = var.instance_port
  to_port                  = var.instance_port
  protocol                 = "tcp"
  source_security_group_id = var.database_sg_id
  security_group_id        = aws_security_group.api_load_balancer_sg.id
}

resource "aws_security_group_rule" "api_container_access_all_ports" {
  type                     = "egress"
  description              = "Outbound access to API containers All Ports"
  from_port                = 0
  to_port                  = 65535
  protocol                 = "tcp"
  source_security_group_id = var.database_sg_id
  security_group_id        = aws_security_group.api_load_balancer_sg.id
}

resource "aws_security_group_rule" "database_deployment_lb_health_check" {
  type              = "ingress"
  description       = "LB-Health Check"
  from_port         = 3001
  to_port           = 3001
  protocol          = "tcp"
  source_security_group_id = aws_security_group.api_load_balancer_sg.id
  security_group_id = var.database_sg_id
  prefix_list_ids   = []
}

resource "aws_security_group_rule" "database_deployment_lb_api" {
  type              = "ingress"
  description       = "LB-API"
  from_port         = 8000
  to_port           = 8000
  protocol          = "tcp"
  source_security_group_id = aws_security_group.api_load_balancer_sg.id
  security_group_id = var.database_sg_id
  prefix_list_ids   = []
}

resource "aws_security_group_rule" "database_deployment_lb_editorial_ui" {
  type              = "ingress"
  description       = "LB-Editorial-UI"
  from_port         = 8080
  to_port           = 8080
  protocol          = "tcp"
  source_security_group_id = aws_security_group.api_load_balancer_sg.id
  security_group_id = var.database_sg_id
  prefix_list_ids   = []
}

resource "aws_security_group_rule" "database_deployment_lb_streamlit_app" {
  type              = "ingress"
  description       = "LB-Streamlit-App"
  from_port         = 8501
  to_port           = 8509
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = var.database_sg_id
  ipv6_cidr_blocks  = []
  prefix_list_ids   = []
}

resource "aws_security_group_rule" "database_deployment_lb_api_documentation" {
  type              = "ingress"
  description       = "LB-API-Documentation"
  from_port         = 8088
  to_port           = 8088
  protocol          = "tcp"
  source_security_group_id = aws_security_group.api_load_balancer_sg.id
  security_group_id = var.database_sg_id
  prefix_list_ids   = []
}

resource "aws_security_group_rule" "database_deployment_lb_graph_vis" {
  type              = "ingress"
  description       = "LB-Graph-Visualisation"
  from_port         = 8086
  to_port           = 8086
  protocol          = "tcp"
  source_security_group_id = aws_security_group.api_load_balancer_sg.id
  security_group_id = var.database_sg_id
  prefix_list_ids   = []
}

data "aws_elb_service_account" "main" {}

resource "aws_s3_bucket" "logs_bucket" {
  bucket = "${var.base_name}-logs"
  acl    = "private"
  force_destroy = true
}

resource "aws_s3_bucket_policy" "policy" {
  bucket = aws_s3_bucket.logs_bucket.id
  policy = data.aws_iam_policy_document.s3_bucket_lb_write.json
}

data "aws_iam_policy_document" "s3_bucket_lb_write" {
  policy_id = "s3_bucket_lb_logs"

  statement {
    actions = [
      "s3:PutObject",
    ]
    effect = "Allow"
    resources = ["${aws_s3_bucket.logs_bucket.arn}/*"]
    sid = "AWSConsoleStmt"

    principals {
      identifiers = ["${data.aws_elb_service_account.main.arn}"]
      type        = "AWS"
    }
  }

  statement {
    actions = [
      "s3:PutObject"
    ]
    effect = "Allow"
    resources = ["${aws_s3_bucket.logs_bucket.arn}/*"]
    sid = "AWSLogDeliveryWrite"
    principals {
      identifiers = ["delivery.logs.amazonaws.com"]
      type        = "Service"
    }
  }

  statement {
    actions = [
      "s3:GetBucketAcl"
    ]
    effect = "Allow"
    resources = ["${aws_s3_bucket.logs_bucket.arn}"]
    sid = "AWSLogDeliveryAclCheck"
    principals {
      identifiers = ["delivery.logs.amazonaws.com"]
      type        = "Service"
    }
  }
}

resource "aws_lb" "api_load_balancer" {
  name                       = "${var.base_name}-api"
  security_groups            = [aws_security_group.api_load_balancer_sg.id]
  subnets                    = var.subnet_ids
  drop_invalid_header_fields = true
  access_logs {
    bucket  = aws_s3_bucket.logs_bucket.bucket
    enabled = true
  }
}

#API target group
resource "aws_lb_target_group" "api_target_group" {
  name        = "${var.base_name}-api"
  port        = 80
  protocol    = "HTTP"
  target_type = "instance"
  vpc_id      = var.vpc_id

  health_check {
    path     = "/"
    protocol = "HTTP"
    port = 8000
    unhealthy_threshold = 2
    healthy_threshold = 5
    timeout = 5
    interval = 30
  }
}

resource "aws_lb_target_group_attachment" "api_target_instance" {
  target_group_arn = aws_lb_target_group.api_target_group.arn
  target_id        = var.instance_id
  port             = 8000
}

#UI target group
resource "aws_lb_target_group" "ui_target_group" {
  name        = "${var.base_name}-ui"
  port        = 80
  protocol    = "HTTP"
  target_type = "instance"
  vpc_id      = var.vpc_id

  health_check {
    path     = "/"
    protocol = "HTTP"
    unhealthy_threshold = 2
    healthy_threshold = 5
    timeout = 5
    interval = 30
  }
}

resource "aws_lb_target_group_attachment" "ui_target_instance" {
  target_group_arn = aws_lb_target_group.ui_target_group.arn
  target_id        = var.instance_id
  port             = 8080
}

#RPC target group
resource "aws_lb_target_group" "rpc_target_group" {
  name        = "${var.base_name}-rpc"
  port        = 3001
  protocol    = "HTTP"
  target_type = "instance"
  vpc_id      = var.vpc_id

  health_check {
    path     = "/"
    protocol = "HTTP"
    unhealthy_threshold = 2
    healthy_threshold = 5
    timeout = 5
    interval = 30
  }
}

resource "aws_lb_target_group_attachment" "rpc_target_instance" {
  target_group_arn = aws_lb_target_group.rpc_target_group.arn
  target_id        = var.instance_id
  port             = 3001
}

# API Documentation target group
resource "aws_lb_target_group" "api_doc_target_group" {
  name        = "${var.base_name}-api-doc"
  port        = 80
  protocol    = "HTTP"
  target_type = "instance"
  vpc_id      = var.vpc_id

  health_check {
    path     = "/"
    protocol = "HTTP"
    unhealthy_threshold = 2
    healthy_threshold = 5
    timeout = 5
    interval = 30
  }
}

resource "aws_lb_target_group_attachment" "api_doc_target_instance" {
  target_group_arn = aws_lb_target_group.api_doc_target_group.arn
  target_id        = var.instance_id
  port             = 8088
}

# Graph Visualisation target group
resource "aws_lb_target_group" "graph_vis_target_group" {
  name        = "${var.base_name}-graph-vis"
  port        = 80
  protocol    = "HTTP"
  target_type = "instance"
  vpc_id      = var.vpc_id

  health_check {
    path     = "/"
    protocol = "HTTP"
    unhealthy_threshold = 2
    healthy_threshold = 5
    timeout = 5
    interval = 30
  }
}

resource "aws_lb_target_group_attachment" "graph_vis_target_instance" {
  target_group_arn = aws_lb_target_group.graph_vis_target_group.arn
  target_id        = var.instance_id
  port             = 8086
}

# Streamlit target group
resource "aws_lb_target_group" "streamlit_target_group" {
  name        = "${var.base_name}-streamlit"
  port        = 8501
  protocol    = "HTTP"
  target_type = "instance"
  vpc_id      = var.vpc_id

  health_check {
    path     = "/"
    protocol = "HTTP"
    unhealthy_threshold = 2
    healthy_threshold = 5
    timeout = 5
    interval = 30
  }
}

resource "aws_lb_target_group_attachment" "streamlit_target_instance" {
  target_group_arn = aws_lb_target_group.streamlit_target_group.arn
  target_id        = var.instance_id
  port             = 8501
}

data "aws_route53_zone" "hosted_zone" {
  name         = var.domain
  private_zone = false
}

resource "aws_route53_record" "api_alias" {
  zone_id = data.aws_route53_zone.hosted_zone.zone_id
  type    = "A"
  name    = "${var.subdomain}.${var.domain}"

  alias {
    name                   = aws_lb.api_load_balancer.dns_name
    zone_id                = aws_lb.api_load_balancer.zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "certificate_validation" {
  for_each = {
    for dvo in aws_acm_certificate.certificate.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 300
  type            = each.value.type
  zone_id         = data.aws_route53_zone.hosted_zone.zone_id
}

resource "aws_acm_certificate" "certificate" {
  domain_name               = var.domain
  subject_alternative_names = ["${var.subdomain}.${var.domain}"]
  validation_method         = "DNS"
}

resource "aws_acm_certificate_validation" "acm_validation" {
  certificate_arn         = aws_acm_certificate.certificate.arn
  validation_record_fqdns = [for record in aws_route53_record.certificate_validation : record.fqdn]
}

resource "aws_lb_listener_certificate" "listener_cert" {
  listener_arn    = aws_lb_listener.api_listener.arn
  certificate_arn = aws_acm_certificate.certificate.arn
}

resource "aws_lb_listener" "api_listener" {
  load_balancer_arn = aws_lb.api_load_balancer.arn
  port              = var.instance_port
  protocol          = "HTTPS"
  certificate_arn   = aws_acm_certificate.certificate.arn

  # Forwarding to UI target group by default
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.ui_target_group.arn
  }
}

#Forwarding to the rpc target group
resource "aws_lb_listener_rule" "rpc_forwarding" {
  listener_arn = aws_lb_listener.api_listener.arn
  priority     = 1

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.rpc_target_group.arn
  }

  condition {
    path_pattern {
      values = ["/rpc*","/user_info*","/docs_with_outstanding_feedback*","/document*","/enrichment_feedback*"]
    }
  }
}

#Forwarding to the api doc target group
resource "aws_lb_listener_rule" "api_doc_forwarding" {
  listener_arn = aws_lb_listener.api_listener.arn
  priority     = 2

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api_doc_target_group.arn
  }

  condition {
    path_pattern {
      values = ["/api_documentation*"]
    }
  }
}

#Forwarding to the api target group
resource "aws_lb_listener_rule" "api_forwarding" {
  listener_arn = aws_lb_listener.api_listener.arn
  priority     = 3

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api_target_group.arn
  }

  condition {
    path_pattern {
      values = ["/api*", "/auth*", "/doc*", "/redoc*"]
    }
  }
}

#Forwarding to the graph visualisation group
resource "aws_lb_listener_rule" "graph_vis_forwarding" {
  listener_arn = aws_lb_listener.api_listener.arn
  priority     = 4

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.graph_vis_target_group.arn
  }

  condition {
    path_pattern {
      values = ["/graph_visualisation*"]
    }
  }
}

#Forwarding to the streamlit target group
resource "aws_lb_listener_rule" "login_forwarding" {
  listener_arn = aws_lb_listener.api_listener.arn
  priority     = 5

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.streamlit_target_group.arn
  }

  condition {
    path_pattern {
      values = ["/streamlit_app*"]
    }
  }
}