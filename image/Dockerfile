FROM public.ecr.aws/lambda/python:3.12

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

# Copy function code
COPY add_user.py ${LAMBDA_TASK_ROOT}
COPY catalog_update.py ${LAMBDA_TASK_ROOT}