# LocalDatabaseAnsS3Synchronization
Python code that allows user's latest local SQL database updates to be synchronized with the version stored as CSV in Amazon S3.


This code establishes a connection to a MySQL database, fetches data from the table, computes a checksum value for the data, and, if the checksum result differs from the previous one, uploads the data to an AWS S3 bucket. 
The necessary libraries are first imported into the code: pymysql for connecting to the MySQL database, boto3 for accessing AWS S3, CSV for reading and writing CSV files, and time for introducing a delay in running the code. The code then sets the MySQL database credentials, the name of the S3 bucket where the data will be uploaded, and the AWS S3 access keys (APIs).

The code then starts an indefinite loop to keep checking for data updates. The pymysql.connect() function and the cursor.execute() and cursor.fetchall() methods are used to retrieve the data from the table while the loop is running. By repeatedly iterating over its description attribute, the cursor object provides the column names as well. The hash() function, which returns a distinct integer value for the string, is then used in the code to determine the data's checksum.

The code uses the csv.writerows() method to write the data to a CSV file called "data.csv" if the current checksum differs from the previous checksum, which was initially initialized as 'None'. It then employs the boto3.client().upload_fileobj() function to upload the CSV file to the S3 bucket.
![image](https://github.com/hifsatm/LocalDatabaseAnsS3Synchronization/assets/108605959/dbb71843-bd08-47f4-b48c-c13312f2e771)

