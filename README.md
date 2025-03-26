# Apache-Airflow-Kafka-Spark-DeltaLake-Real-Time-Stream-Pipeline

This repository implements a real-time stream pipeline using Apache Airflow, Apache Kafka, Apache Spark, and Delta Lake. The project is designed for data ingestion, transformation, and storage of real-time and historical traffic and social media data, leveraging the power of Delta Lake for data management.

## Setup
### Clone the repository

```bash
git clone https://github.com/tashi-2004/Apache-Airflow-Kafka-Spark-DeltaLake-Real-Time-Stream-Pipeline.git
```
## Data Ingestion

The data ingestion workflow is divided into **airflow**, **Coldpath** and **Hotpath**.
### 1. Airflow Dags
- Each script in the `data_ingestion/airflows` folder defines an Airflow DAG that orchestrates the data ingestion process.

  - `fetch_twitter.py`: Fetches data from Twitter at a scheduled interval.
  - `fetch_traffic_2025.py`: Fetches and ingests traffic data for 2025.
  - `fetch_serapi.py`: Fetches traffic-related images from SERAPI.
  - `fetch_google_maps.py`: Fetches data from Google Maps API.
  - `fetch_bluesky.py`: Fetches posts from BlueSky.
  - `coldpath.py`: Dag for coldpath.

### 2. Coldpath
- **Coldpath**: Ingests static data files or historical data from sources like traffic data, social media, and images. Coldpath ingestion is implemented in the `data_ingestion/cold_paths` folder, including:

  - `ingest_cold_traffic_data.py`: Ingests historical traffic data.
  - `ingest_cold_twitter_data.py`: Ingests cold Twitter data.
  - `ingest_cold_google_maps_images.py`: Ingests cold Google Maps images.
  - `ingest_cold_serapi_images.py`: Ingests cold SERAPI traffic images.
### 3. Hotpath
- **Hotpath**: Streams real-time data using producers and consumers. Hotpath ingestion involves:
  - **Producers**: 
      - `produce_traffic_stream.py`: Streams traffic data from CSV to Kafka.
      - `produce_bluesky_stream.py`: Streams BlueSky data to Kafka.
  - **Consumers**: 
      - `consume_traffic_stream.py`: Consumes traffic data from Kafka.
      - `consume_bluesky_stream.py`: Consumes BlueSky data from Kafka.

## Data Processing
The data processing logic is handled in `transform.py`, which:
  - Loads raw data from sources.
  - Transforms data using Apache Spark.
  - Stores the processed data in Delta Lake.
  - Generates metadata files for each dataset.


## Storage
The storage structure is managed in Delta Lake. Raw data, metadata, and processed data are stored in the `storage/delta` directory, categorized by data source and year.

### Explanation:

1. **`metadata/`**: Contains metadata files for each data source. These metadata files hold important information like the number of records, data types, sample data, file sizes, and timestamps.
     - Files:
       - `bluesky_data_metadata.json`: Metadata for Bluesky data.
       - `serapi_data_metadata.json`: Metadata for serapi data.
       - `traffic_2024_data_metadata.json`: Metadata for 2024 traffic data.
       - `traffic_2025_data_metadata`: Metadata for 2025 traffic data.
       - `twitter_data_metadata.json`: Metadata for Twitter data.
       - `google_maps_data_metadata`: Metadata for google maps.

2. **`raw/`**: Stores raw data before any transformation or processing. 
   **`traffic_data/`**: Contains the traffic data, split by years (2024 and 2025). The data here is fetched from OpenData Barcelona.
   - **`2024/`**: Stores batch traffic data for 2024.
   - **`2025/`**: Stores streaming traffic data for 2025.
   - **`social_media_data/`**: Stores social media data from different platforms.
      - **`twitter/`**: Contains data extracted from Twitter.
      - **`bluesky/`**: Contains data extracted from BlueSky (another social media platform).
   - **`images/`**: Stores images fetched from APIs like Google Maps and SERAPI.
       - **`google_maps/`**: Contains images retrieved from Google Maps API.
       - **`serapi/`**: Contains traffic images retrieved from SERAPI API.

## Project Structure

| File/Directory                                         | Description                                           |
| ------------------------------------------------------ | ----------------------------------------------------- |
| `.gitignore`                                           | Ignore unnecessary files in version control          |
| `README.md`                                             | Project documentation                                 |
| `requirements.txt`                                      | Python dependencies required for the project          |
| **configs/**                                             | Configuration files for different components          |
| `configs/airflow.cfg`                                  | Configuration file for Apache Airflow                 |
| `configs/delta-lake.yml`                               | Configuration file for Delta Lake                     |
| `configs/spark-defaults.conf`                          | Configuration file for Apache Spark                   |
| **data_ingestion/**                                     | Data ingestion scripts (Coldpath & Hotpath)           |
| `data_ingestion/airflows/`                             | Airflow DAGs for orchestrating ingestion workflows    |
| `data_ingestion/airflows/dags/`                        | Folder for Airflow DAG scripts                        |
| `data_ingestion/airflows/dags/fetch_traffic_2024.py`   | Fetches 2024 traffic data                            |
| `data_ingestion/airflows/dags/fetch_traffic_2025.py`   | Fetches 2025 traffic data                            |
| `data_ingestion/airflows/dags/fetch_twitter.py`       | Fetches Twitter data                                  |
| `data_ingestion/airflows/dags/fetch_bluesky.py`       | Fetches BlueSky data                                  |
| `data_ingestion/airflows/dags/fetch_google_maps.py`   | Fetches Google Maps data                              |
| `data_ingestion/airflows/dags/fetch_serapi.py`        | Fetches SERAPI data                                   |
| `data_ingestion/airflows/dags/coldpath.py`            | Coldpath ingestion script                             |
| **data_ingestion/cold_paths/**                         | Coldpath ingestion scripts                            |
| `data_ingestion/cold_paths/ingest_cold_traffic_data.py` | Ingests cold traffic data                             |
| `data_ingestion/cold_paths/ingest_cold_twitter_data.py` | Ingests cold Twitter data                             |
| `data_ingestion/cold_paths/ingest_cold_google_maps_images.py` | Ingests cold Google Maps images                      |
| `data_ingestion/cold_paths/ingest_cold_serapi_images.py` | Ingests cold SERAPI images                            |
| **data_ingestion/hot_paths/**                          | Hotpath data streaming scripts                        |
| `data_ingestion/hot_paths/producer/`                   | Producers for data streaming                         |
| `data_ingestion/hot_paths/producer/produce_traffic_stream.py` | Streams traffic data to Kafka                        |
| `data_ingestion/hot_paths/producer/produce_bluesky_stream.py` | Streams BlueSky data to Kafka                        |
| `data_ingestion/hot_paths/consumer/`                   | Consumers for data ingestion                         |
| `data_ingestion/hot_paths/consumer/consume_traffic_stream.py` | Consumes traffic data from Kafka                     |
| `data_ingestion/hot_paths/consumer/consume_bluesky_stream.py` | Consumes BlueSky data from Kafka                     |
| **data_processing/**                                   | Data processing scripts                              |
| `data_processing/transform.py`                        | Data transformation logic                             |
| **storage/**                                            | Data storage structure in Delta Lake                 |
| `storage/delta/`                                       | Delta Lake storage directory                          |
| `storage/delta/raw/`                                   | Raw data storage (before processing)                  |
| `storage/delta/raw/metadata/`                          | Metadata files for each data source                   |
| `storage/delta/raw/metadata/traffic_2024_metadata.json` | Metadata for 2024 traffic data                        |
| `storage/delta/raw/metadata/traffic_2025_metadata.json` | Metadata for 2025 traffic data                        |
| `storage/delta/raw/metadata/twitter_metadata.json`     | Metadata for Twitter data                             |
| `storage/delta/raw/metadata/bluesky_metadata.json`     | Metadata for BlueSky data                             |
| `storage/delta/raw/metadata/google_maps_metadata.json` | Metadata for Google Maps images                       |
| `storage/delta/raw/metadata/serapi_metadata.json`      | Metadata for SERAPI traffic images                    |
| `storage/delta/traffic_data/`                          | Traffic data storage                                  |
| `storage/delta/traffic_data/2024/`                     | Batch traffic data from OpenData Barcelona (2024)     |
| `storage/delta/traffic_data/2025/`                     | Streaming traffic data from OpenData Barcelona (2025) |
| `storage/delta/social_media_data/`                     | Social media data storage                             |
| `storage/delta/social_media_data/twitter/`             | Data extracted from Twitter                           |
| `storage/delta/social_media_data/bluesky/`             | Data extracted from BlueSky                           |
| `storage/delta/images/`                                | Image data storage                                    |
| `storage/delta/images/google_maps/`                    | Images retrieved from Google Maps API                 |
| `storage/delta/images/serapi/`                         | Traffic images retrieved from SERAPI API              |


## Contact
For queries or contributions, please contact:
**Tashfeen Abbasi**  
Email: abbasitashfeen7@gmail.com
