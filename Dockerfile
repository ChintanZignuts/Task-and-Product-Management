# Use official Python image as base
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy project files to the container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "task_product_manager.wsgi:application"]