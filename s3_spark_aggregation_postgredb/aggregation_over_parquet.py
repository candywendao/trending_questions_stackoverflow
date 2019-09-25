#!/usr/bin/python

from pyspark import SparkConf, SparkContext
from pyspark.sql.session import SparkSession
import os
import sys

# add jars
conf = SparkConf().set(
    "spark.jars", \
    "/usr/local/spark/jars/hadoop-aws-2.7.3.jar,"+\
    "/usr/local/spark/jars/aws-java-sdk-1.7.4.jar,"+\
    "/usr/local/spark/jars/postgresql-42.2.8.jar"\
).set(
    "spark.driver.extraClassPath",\
    "/usr/local/spark/jars/postgresql-42.2.8.jar"\
).setMaster("spark://10.0.0.17:7077").setAppName(\
    "aggregate_votes_comments"\
)

sc = SparkContext(conf=conf)
spark = SparkSession.builder.getOrCreate()

END_DATE = sys.argv[1] if len(sys.argv) > 1 else "2016-06-20"

#VOTES_FILEPATH = "/home/ubuntu/stackoverflow/data/votes"
#COMMENTS_FILEPATH = "/home/ubuntu/stackoverflow/data/comments"

COMMENTS_FILEPATH = "s3a://stack-overflow-parquets-bydate/comments"
POSTS_FILEPATH = 's3a://stack-overflow-parquets-bydate/posts_all'
VOTES_FILEPATH = "s3a://stack-overflow-parquets-bydate/votes"

#POSTGRESQL_URL = 'jdbc:postgresql://localhost/demo'
POSTGRESQL_URL = 'jdbc:postgresql://insight.cgslpa7fcmfh.us-west-2.rds.amazonaws.com/stackoverflow'


#votes = spark.read.parquet("s3a://stack-overflow-parquets-bydate/votes")
votes = spark.read.parquet(VOTES_FILEPATH)
votes.createOrReplaceTempView("votes")
votes_7d = spark.sql(""" \
    SELECT _PostId, COUNT(1) AS num_votes, '{end_date}' AS date \
    FROM votes \
    WHERE date <= '{end_date}' \
    AND date > date_sub('{end_date}', 7) \
    AND _VoteTypeId = 5 \
    GROUP BY _PostId \
    ORDER BY num_votes DESC \
    """.format(end_date=END_DATE))
votes_7d.show()


comments = spark.read.parquet(COMMENTS_FILEPATH)
comments.createOrReplaceTempView("comments")
comments_7d = spark.sql(""" \
    SELECT _PostId, COUNT(1) AS num_comments, '{end_date}' AS date \
    FROM comments \
    WHERE date <= '{end_date}' \
    AND date > date_sub('{end_date}', 7) \
    GROUP BY _PostId \
    ORDER BY num_comments DESC \
    """.format(end_date=END_DATE))
comments_7d.show()


# outer-join votes with comments data and then inner-join with post to get tags info
votes_7d.createOrReplaceTempView("votes_7d")
comments_7d.createOrReplaceTempView("comments_7d")
posts = spark.read.parquet(POSTS_FILEPATH)
posts.createOrReplaceTempView("posts")
posts.show();

votes_and_comments_7d = spark.sql(""" \
    SELECT \
        a._PostId, \
        posts._Title,\
        posts._Body,\
        a.num_votes AS num_votes_7d, \
        a.num_comments AS nun_comments_7d, \
        posts._CommentCount AS total_comments, \
        posts._FavoriteCount AS total_votes, \
        split(substring(posts._tags, 2, length(posts._tags) - 2), '><') AS tags, \
        a.date AS date \
    FROM ( \
        SELECT 
            ifnull(x._PostId, y._PostId) AS _PostId, \
            x.num_votes, \
            y.num_comments, \
            ifnull(x.date, y.date) AS date \
        FROM votes_7d AS x \
        FULL OUTER JOIN comments_7d AS y \
        ON x._PostId = y._PostId \
        AND x.date = y.date \
    ) AS a INNER JOIN posts \
    ON a._PostId = posts._Id \
    AND posts._PostTypeId = 1 \
""".format(end_date=END_DATE))
votes_and_comments_7d.show()
votes_and_comments_7d.printSchema()

votes_and_comments_7d.write \
    .partitionBy("date") \
    .mode("overwrite") \
    .format("jdbc") \
    .option("url", POSTGRESQL_URL) \
    .option("dbtable", "test_stackoverflow_v4") \
    .option("user", "postgres") \
    .option("password", os.environ.get("AWS_RDS_POSTGRES_PASSWORD")) \
    .save()
