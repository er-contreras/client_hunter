FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install llama-cpp-python
CMD ["python", "score.py"]

