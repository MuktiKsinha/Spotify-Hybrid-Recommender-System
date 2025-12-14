# set up the base image
FROM python:3.12

# set the working directory
WORKDIR /app/

# copy the requirements file to workdir
COPY requirements.txt .

# install the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire data folder
COPY ./data/ ./data/

# Copy all required Python scripts
COPY app.py \
     collaborative_filtering.py \
     content_based_filtering.py \
     hybrid_recommendation.py \
     data_cleaning.py \
     transform_filtered_data.py \
     ./

# expose the port on the container
EXPOSE 8000

# run the streamlit app
CMD ["streamlit", "run", "app.py", "--server.port", "8000", "--server.address", "0.0.0.0"]
