import pymysql
import boto3
import csv
import time

# AWS S3 credentials
access_key = "XXX"
secret_key = "XYZ"

# MySQL database credentials
db_host = "localhost"
db_user = "hifsa"
db_password = "XYZ"
db_name = "sys"

# S3 bucket name
bucket_name = "tablesforaubotproject"

# initialize a variable to hold the previous checksum value
previous_checksum = None

while True:
    try:
        # connect to MySQL database
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, db=db_name)

        # retrieve data from MySQL database
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM new_table;")
        data = cursor.fetchall()
        columns = [i[0] for i in cursor.description]  # get the column names from the cursor

        # calculate checksum of the data
        current_checksum = hash(str(data))

        # if the checksum is different than the previous one, write data to a CSV file and upload to S3 bucket
        if current_checksum != previous_checksum:
            with open("data.csv", "w") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(columns)  # write the column names as the first row
                csv_writer.writerows(data)

            s3 = boto3.client("s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key)
            with open("data.csv", "rb") as data_file:
                s3.upload_fileobj(data_file, bucket_name, "data.csv")
                print("Data successfully uploaded to S3 bucket.")

            # set previous_checksum to current_checksum
            previous_checksum = current_checksum

        # wait for 5 seconds before checking again
        time.sleep(5)

    except Exception as e:
        print("Error occurred:", e)
    finally:
        # close database connection
        if 'conn' in locals() and conn:
            conn.close()
