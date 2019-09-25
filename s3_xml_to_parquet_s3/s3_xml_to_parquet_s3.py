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
)
#.setMaster(\
#    "spark://10.0.0.17:7077"\
#).setAppName(\
#    "read_xml_from_s3_write_parquet"\
#)

sc = SparkContext(conf=conf)

spark = SparkSession.builder.getOrCreate()

votes_file = "s3a://stack-overflow-datadump-xml/stackoverflow.com-Votes/Votes.xml"
comments_file = "s3a://stack-overflow-datadump-xml/stackoverflow.com-Comments/Comments.xml"
posts_file = "s3a://stack-overflow-datadump-xml/stackoverflow.com-Posts/Posts.xml"
#votes_file = "s3a://stack-overflow-datadump-xml/3dprinting.stackexchange.com/Votes.xml"
#comments_file = "s3a://stack-overflow-datadump-xml/3dprinting.stackexchange.com/Comments.xml"
#posts_file = "s3a://stack-overflow-datadump-xml/3dprinting.stackexchange.com/Posts.xml"


### load xml files from s3 bucket
df_votes = spark.read \
    .format('xml') \
    .options(rowTag='row') \
    .load(votes_file)
df_votes = df_votes.withColumn('date', df_votes['_CreationDate'].cast('date'))

df_comments = spark.read \
    .format('xml') \
    .options(rowTag='row') \
    .load(comments_file)

df_comments = df_comments.withColumn('date', df_comments['_CreationDate'].cast('date'))

df_posts = spark.read \
    .format('xml') \
    .options(rowTag='row') \
    .load(posts_file)

### write parquet files partitionby date
#df_votes.write.mode('append').partitionBy("date").parquet("s3a://stack-overflow-parquets-bydate/votes_3dprinting")
#df_comments.write.mode('append').partitionBy("date").parquet("s3a://stack-overflow-parquets-bydate/comments_3dprinting")

#df_posts.write.parquet("s3a://stack-overflow-parquets-bydate/posts_3dprinting")


df_votes.write.mode('append').partitionBy("date").parquet("/home/ubuntu/stackoverflow/data/votes")
df_comments.write.mode('append').partitionBy("date").parquet("/home/ubuntu/stackoverflow/data/comments")
df_posts.write.parquet("/home/ubuntu/stackoverflow/data/posts")
