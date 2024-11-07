FROM public.ecr.aws/lambda/python:3.12

# Install git
RUN microdnf install git -y

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

# Copy function code
COPY . ${LAMBDA_TASK_ROOT}

ENV GOOGLE_APPLICATION_CREDENTIALS gcp_config.json