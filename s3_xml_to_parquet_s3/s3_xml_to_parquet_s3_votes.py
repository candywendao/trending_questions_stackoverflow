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

votes_file = "s3a://stack-overflow-datadump-xml/stackoverflow.com-Votes/Votes.xml"
#votes_file = "s3a://stack-overflow-datadump-xml/3dprinting.stackexchange.com/Votes.xml"


### load xml files from s3 bucket
df_votes = spark.read \
    .format('xml') \
    .options(rowTag='row') \
    .load(votes_file)
df_votes = df_votes.withColumn('date', df_votes['_CreationDate'].cast('date'))
df_votes.describe(["date"]).show()



### write parquet files partitionby date
#df_votes.write.mode('append').partitionBy("date").parquet("s3a://stack-overflow-parquets-bydate/votes_3dprinting")



#df_votes.write.mode('append').partitionBy("date").parquet("/home/ubuntu/stackoverflow/data/votes")
