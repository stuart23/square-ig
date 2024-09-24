# resource "aws_s3_bucket" "website_bucket" {
#   bucket = var.domain_name
# }


# resource "aws_s3_bucket_versioning" "website_bucket_versioning" {
#   bucket = aws_s3_bucket.website_bucket.id
#   versioning_configuration {
#     status = "Enabled"
#   }
# }


# resource "aws_s3_bucket_public_access_block" "website_bucket_acl" {
#   bucket = aws_s3_bucket.website_bucket.id

#   block_public_acls       = false
#   block_public_policy     = false
#   ignore_public_acls      = false
#   restrict_public_buckets = false
# }


# resource "aws_s3_bucket_ownership_controls" "website_bucket_ownership" {
#   bucket = aws_s3_bucket.website_bucket.id
#   rule {
#     object_ownership = "BucketOwnerPreferred"
#   }
# }


# resource "aws_s3_bucket_acl" "website_bucket_acl" {
#   bucket = aws_s3_bucket.website_bucket.id
#   depends_on = [
#     aws_s3_bucket_ownership_controls.website_bucket_ownership,
#     aws_s3_bucket_public_access_block.website_bucket_acl
#   ]
#   acl = "public-read"
# }


# resource "aws_s3_bucket_policy" "website_bucket_policy" {
#   bucket     = aws_s3_bucket.website_bucket.id
#   depends_on = [aws_s3_bucket_ownership_controls.website_bucket_ownership]
#   policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Sid    = "AllowPublicRead"
#         Effect = "Allow"
#         Resource = [
#           aws_s3_bucket.website_bucket.arn,
#           "${aws_s3_bucket.website_bucket.arn}/*",
#         ]
#         Action    = ["S3:GetObject"]
#         Principal = "*"
#       }
#     ]
#   })
# }


# resource "aws_s3_bucket_website_configuration" "website_bucket_config" {
#   bucket = aws_s3_bucket.website_bucket.id
#   index_document {
#     suffix = "index.html"
#   }
#   error_document {
#     key = "error.html"
#   }
# }


# output "s3_bucket_id" {
#   value = aws_s3_bucket_website_configuration.website_bucket_config.website_endpoint
# }