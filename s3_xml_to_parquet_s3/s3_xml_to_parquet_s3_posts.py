#!/usr/bin/python

from pyspark import SparkConf, SparkContext
from pyspark.sql.session import SparkSession
import boto3

# add jars
conf = SparkConf().set(\
    "spark.jars",\
    "/usr/local/spark/jars/spark-xml_2.11-0.6.0.jar,"+\
    "/usr/local/spark/jars/hadoop-aws-2.7.3.jar,"+\
    "/usr/local/spark/jars/aws-java-sdk-1.7.4.jar"\
).setMaster(\
    "spark://10.0.0.17:7077"\
).setAppName(\
    "read_xml_from_s3_write_parquet"\
)

sc = SparkContext(conf=conf)

spark = SparkSession.builder.getOrCreate()

posts_file = "s3a://stack-overflow-datadump-xml/stackoverflow.com-Posts/Posts.xml"

### load xml files from s3 bucket

df_posts = spark.read \
    .format('xml') \
    .options(rowTag='row') \
    .load(posts_file)

### write parquet files
df_posts.write.parquet("s3a://stack-overflow-parquets-bydate/posts_all")
