# AWS base image for lambda functions
# https://docs.aws.amazon.com/lambda/latest/dg/images-create.html#runtimes-images-provided
FROM public.ecr.aws/lambda/provided:al2023

RUN dnf install -y tar gzip unzip

# Get the Astro CLI
RUN curl -sSL install.astronomer.io | bash -s

# # Get the AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -fr aws*

# Copy our lambda function across
COPY lambda_function.sh /var/task/lambda_function.sh
RUN chmod 755 /var/task/lambda_function.sh

# Copy the custom bootstrap - see this tutorial about custom lambda runtimes:
# https://docs.aws.amazon.com/lambda/latest/dg/runtimes-walkthrough.html
COPY ./bootstrap /var/runtime/bootstrap
RUN chmod 755 /var/runtime/bootstrap


CMD ["lambda_function.sh"]