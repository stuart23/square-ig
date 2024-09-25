locals {
  lambda_logging_format = jsonencode({
    requestId        = "$context.requestId"
    requestTime      = "$context.requestTime"
    requestTimeEpoch = "$context.requestTimeEpoch"
    path             = "$context.path"
    method           = "$context.httpMethod"
    status           = "$context.status"
    responseLength   = "$context.responseLength"
  })
}