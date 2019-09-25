#!/usr/bin/env python

# import libraries
import subprocess
import boto3
import wget
import os
#import shutil
from extract_url import extract_url

'''
This script ...

'''

# Create an S3 client
s3 = boto3.client('s3')

# Create an S3 bucket
bucket_name = 'stack-overflow-datadump-xml'

### run the 3 lines below only once when creating new S3 bucket
##region='us-west-2'
##location = {'LocationConstraint': region}
##s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)

# Files to be uploaded
source_url = 'https://archive.org/download/stackexchange/'
file_names = extract_url(source_url)

#print ((file_names))
for filename in file_names:
    dir_name = filename[:-3]
    url = source_url + filename
    print('Downloading ' + filename + '...')
    wget.download(url)
    process_7z_file_shell = "./process_7z_file_batch.sh"
    subprocess.call([process_7z_file_shell], shell=True)
    #print('Uploading ' + dir_name + ' to S3...')
    #s3.upload_file(dir_name/*.xml, bucket_name, filename)
    os.remove(filename) 
   

