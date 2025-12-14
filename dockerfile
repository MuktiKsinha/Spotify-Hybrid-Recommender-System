# set up the base image
FROM python:3.12

WORKDIR /app/

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only required data files (exclude huge raw files)
COPY ./data/cleaned_data.csv ./data/
COPY ./data/collab_filtered_data.csv ./data/
COPY ./data/interaction_matrix.npz ./data/
COPY ./data/track_ids.npy ./data/
COPY ./data/transformed_data.npz ./data/
COPY ./data/transformed_hybrid_data.npz ./data/

# Copy scripts
COPY app.py \
     collaborative_filtering.py \
     content_based_filtering.py \
     hybrid_recommendation.py \
     data_cleaning.py \
     transform_filtered_data.py \
     ./

EXPOSE 8000

CMD ["streamlit", "run", "app.py", "--server.port", "8000", "--server.address", "0.0.0.0"]

