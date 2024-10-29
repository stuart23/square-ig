resource "aws_cloudfront_distribution" "s3_distribution" {
  depends_on = [module.acm.certificate_validation]
  origin {
    domain_name = aws_s3_bucket.website_bucket.bucket_regional_domain_name
    origin_id   = var.domain_name
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"

  # logging_config {
  #   include_cookies = false
  #   bucket          = "mylogs.s3.amazonaws.com"
  #   prefix          = "myprefix"
  # }

  aliases = [var.domain_name]

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = var.domain_name

    function_association {
      event_type   = "viewer-request"
      function_arn = aws_cloudfront_function.rewrite_url.arn
    }

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  price_class = "PriceClass_100"

  restrictions {
    geo_restriction {
      restriction_type = "none"
      locations        = []
    }
  }

  viewer_certificate {
    acm_certificate_arn = module.acm.certificate_arn
    ssl_support_method  = "sni-only"
  }
}


resource "aws_cloudfront_function" "rewrite_url" {
  name    = "rewrite_url"
  runtime = "cloudfront-js-2.0"
  publish = true
  code    = file("${path.module}/function.js")
}


resource "porkbun_dns_record" "cloudfront_alias" {
  domain  = var.domain_name
  content = aws_cloudfront_distribution.s3_distribution.domain_name
  type    = "ALIAS"
}