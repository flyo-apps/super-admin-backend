FROM public.ecr.aws/z7v3g1r9/fastapi-tiangolo:v1
LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
RUN pip3 install --upgrade pip
RUN pip3 install pipenv
COPY ./ Pipfile* Pipfile.lock /app/
RUN cd /app/ && pipenv install --ignore-pipfile --system
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app", "--app-dir", "src/"]