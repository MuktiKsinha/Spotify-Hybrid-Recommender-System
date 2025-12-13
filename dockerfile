# -----------------------------
# Stage 1: Build stage
# -----------------------------
FROM python:3.12-slim AS builder

#setup working directory
WORKDIR /app/

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        git \
        curl \
        && rm -rf /var/lib/apt/lists/*


# copy the requirement file to dir
COPY requirements.txt .

# install the requirements
RUN pip install --upgrade pip \
    && pip install --prefix=/install --no-cache-dir -r requirements.txt

# Copy all required data files at once
COPY ./data/collab_filtered_data.csv \
     ./data/interaction_matrix.npz \
     ./data/track_ids.npy \
     ./data/cleaned_data.csv \
     ./data/transformed_data.npz \
     ./data/transformed_hybrid_data.npz \
     ./data/

# copy all the required python scrips
COPY app.py \
     collaborative_filtering.py \
     content_based_filtering.py \
     hybrid_recommendation.py \
     data_cleaning.py \
     transform_filtered_data.py \
     ./

# -----------------------------
# Stage 2: Runtime stage
# -----------------------------
FROM python:3.12-slim

WORKDIR /app

# Copy only installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy application code and data
COPY --from=builder /app ./ 

# Expose Streamlit port
EXPOSE 8000

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port", "8000", "--server.address", "0.0.0.0"]