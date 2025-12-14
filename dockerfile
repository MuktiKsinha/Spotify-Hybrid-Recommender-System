# Dockerfile
FROM python:3.12

WORKDIR /app/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python scripts only
COPY app.py \
     collaborative_filtering.py \
     content_based_filtering.py \
     hybrid_recommendation.py \
     data_cleaning.py \
     transform_filtered_data.py \
     ./

EXPOSE 8000

# run the streamlit app
CMD [ "streamlit", "run", "app.py", "--server.port", "8000", "--server.address", "0.0.0.0"]