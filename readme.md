# Content Feed on Stack Overflow

### Project Overview


This project creates data pipelines using Stack Overflow’s content data dump to recommend contents such as most trending questions under various domains and builds a web application using Flask that displays popular questions that combine user-selected topic tags.


- [Slides](https://docs.google.com/presentation/d/1HqPJ7OJsYK-dsdT9ysA3lBjUMGt-rKgHDMsvEJq_Eeg/edit?usp=sharing)
- [Demo](http://www.datasolutions.club/posts)


### File Structure

The directory structure of the repo:

    ├── README.md
    ├── url_7z_xml_to_s3
    │   └── transfer_to_s3.py
	|   └── extract_url.py
	|   └── process_7z_file_batch.sh
    ├── s3_xml_to_parquet_s3
    │   └── s3_xml_to_parquet_s3.py
    ├── s3_spark_aggregation_postgredb
    │   └── aggregation_over_parquet_v2.py
    ├── postgredb_to_flask_web
        └── flaskr
	        └── __init__.py
	        └── db.py
            └── posts.py
            └── templates
            |   ├── base.html
            |   ├── posts.html
            └── static
            |   ├── style.css
    ├── airflow
        └── dag
	        └── aggregation_daily_job.py

### Data Source & Size

[Stack Exchange Data Dump](https://archive.org/details/stackexchange): 100 GB

### Engineering Challenge

-   Fast distributed computation over large datasets (data preprocessing, aggregation)
-   Scheduler for daily-batch processing
-   Flexible/Robust data schema design to incorporate dynamic business needs
-   Generic platform for top-feed related products

### Tech Stack Overview

![Tech Stack](https://github.com/candywendao/trending_questions_stackoverflow/blob/master/pics/tech_stack_overview.png)

### Future Improvement

- Enable data ingestion from multiple sources
- Build pipelines to support ML-based feed/post recommendation
- Streaming data support to satisfy real-time business needs
