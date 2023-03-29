from datetime import datetime
from google.cloud import storage
from mongodb import *
from pyspark.sql import Row, SparkSession

from user_definition import *


def retreive_pubmed(spark, bucket_name, date):
    pubmed_df1 = (
        spark.read.format("csv")
        .option("header", True)
        .load(f"gs://{bucket_name}/pubmed_data/{search_term1}_{date}.csv")
    )
    pubmed_df2 = (
        spark.read.format("csv")
        .option("header", True)
        .load(f"gs://{bucket_name}/pubmed_data/{search_term2}_{date}.csv")
    )

    return pubmed_df1, pubmed_df2


def insert_aggregates_to_mongo():
    spark = SparkSession.builder.getOrCreate()
    conf = spark.sparkContext._jsc.hadoopConfiguration()
    conf.set("google.cloud.auth.service.account.json.keyfile",
             service_account_key_file)
    conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
    conf.set("fs.AbstractFileSystem.gs.impl",
             "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")

    today = datetime.now()

    pubmed_df1, pubmed_df2 = retreive_pubmed(
        spark, bucket_name, today.strftime("%Y-%m-%d"))

    # mongoDB comments collection
    mongodb_df1 = MongoDBCollection(mongo_username,
                                    mongo_password,
                                    mongo_ip_address,
                                    database_name,
                                    collection_1_name)

    df1_aggregates = pubmed_df1.rdd.map(lambda x: x.asDict())

    for aggregate in df1_aggregates.collect():
        print(aggregate)
        mongodb_df1.insert_one(aggregate)

    # mongoDB posts collection
    mongodb_df2 = MongoDBCollection(mongo_username,
                                    mongo_password,
                                    mongo_ip_address,
                                    database_name,
                                    collection_2_name)

    df2_aggregates = pubmed_df2.rdd.map(lambda x: x.asDict())

    for aggregate in df2_aggregates.collect():
        print(aggregate)
        mongodb_df2.insert_one(aggregate)


if __name__ == "__main__":
    insert_aggregates_to_mongo()
