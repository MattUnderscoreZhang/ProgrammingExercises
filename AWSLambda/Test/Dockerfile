FROM public.ecr.aws/lambda/python:3.9
#FROM public.ecr.aws/amazon/aws-lambda-python:3.9

# Install the function's dependencies using file poetry.lock from your project folder.
COPY poetry.lock pyproject.toml ${LAMBDA_TASK_ROOT}
RUN pip install poetry
RUN poetry config virtualenvs.create false  # install dependencies to current virtualenv
RUN poetry install --no-dev

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]
