# from datetime import date, datetime, timedelta
import os
from Bio import Entrez
# yesterday = date.today() - timedelta(days=1)
# # two_days_ago = date.today() - timedelta(days=4)
# # three_days_ago = date.today() - timedelta(days=5)
# two_days_ago = '2023-01-26'
# three_days_ago = '2023-01-25'

# sf_data_url = "data.sfgov.org"
# data_limit = 200000
# sf_data_sub_uri = "gnap-fj3t"
# sf_data_app_token = os.environ.get("SF_DATA_TOKEN")

# noaa_token = os.environ.get("NOAA_TOKEN")
# station_id = "GHCND:USW00023272"
# dataset_id = "GHCND"
# location_id = "CITY:US060031"
# noaa_endpoint = f"data?datasetid={dataset_id}&datatypeid=PRCP&station_id={station_id}&startdate={three_days_ago}&enddate={two_days_ago}"
# noaa_api_url = f"https://www.ncei.noaa.gov/cdo-web/api/v2/{noaa_endpoint}"


bucket_name = os.environ.get("GS_BUCKET_NAME")
service_account_key_file = os.environ.get("GS_SERVICE_ACCOUNT_KEY_FILE")

mongo_username = os.environ.get("MONGO_USERNAME")
mongo_password = os.environ.get("MONGO_PASSWORD")
mongo_ip_address = os.environ.get("MONGO_IP")
database_name = os.environ.get("MONGO_DB_NAME")

search_term1 = "non-small cell lung cancer"
search_term2 = "pulmonary fibrosis"


collection_1_name = "abstracts_non_small_lung_cancer"
collection_2_name = "abstracts_pulmonary_fibrosis"


dag_folder = "/Users/lingrajsvannur/Documents/DistributedDataProject/2023-msds697-distributed-data-systems/"
