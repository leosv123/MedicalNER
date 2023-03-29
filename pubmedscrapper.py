from Bio import Entrez
import pandas as pd
from google.cloud import storage


from user_definition import *
from datetime import datetime, date


# set this for airflow errors. https://github.com/apache/airflow/discussions/24463
os.environ["no_proxy"] = "*"


def scrape_abstract(search_term="non-small cell lung cancer"):
    data = []
    # Set up email address to identify the user to PubMed
    Entrez.email = "lsvannur98@gmail.com"
    Entrez.timeout = 3600

    # Search for articles related to non-small cell lung cancer
    search_term = search_term
    handle = Entrez.esearch(db="pubmed", term=search_term, retmax=2000)
    record = Entrez.read(handle)
    handle.close()

    # Get a list of the PubMed IDs for the search results
    id_list = record["IdList"]

    # Fetch the abstracts for the articles and print them out
    for pmid in id_list:
        temp = {}
        handle = Entrez.efetch(db="pubmed", id=pmid, retmode="xml")
        record = Entrez.read(handle)
        handle.close()
        # print(record)
        # # Extract relevant information from the article record
        try:
            article_title = record["PubmedArticle"][0]["MedlineCitation"]["Article"]["ArticleTitle"]
        except:
            article_title = None
        try:
            article_abstract = record["PubmedArticle"][0]["MedlineCitation"]["Article"]["Abstract"]["AbstractText"]
        except:
            article_abstract = None
        try:
            article_authors = record["PubmedArticle"][0]["MedlineCitation"]["Article"]["AuthorList"]
        except:
            article_authors = None

        # # Print out the information
        temp['article_title'] = article_title
        temp['article_abstract'] = article_abstract
        temp['article_authors'] = article_authors
        data.append(temp)

    df = pd.DataFrame(data)
    df['article_abstract'] = df['article_abstract'].apply(
        lambda x: x[0] if x is not None else None)
    return df


def write_csv_to_gcs(bucket_name, blob_name, service_account_key_file, df):
    """Write and read a blob from GCS using file-like IO"""
    storage_client = storage.Client.from_service_account_json(
        service_account_key_file)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    with blob.open("w") as f:
        df.to_csv(f, index=False)

def pubmed_upload_data():
    today = datetime.now()
    abstracts_df1 = scrape_abstract(search_term1)
    abstracts_df2 = scrape_abstract(search_term2)
    


    abstracts1_blob_name = f'pubmed_data/{search_term1}_{today.strftime("%Y-%m-%d")}.csv'
    abstracts2_blob_name = f'pubmed_data/{search_term2}_{today.strftime("%Y-%m-%d")}.csv'
    
    write_csv_to_gcs(bucket_name, abstracts1_blob_name,
                     service_account_key_file, abstracts_df1)

    
    write_csv_to_gcs(bucket_name, abstracts2_blob_name,
                     service_account_key_file, abstracts_df2)
    