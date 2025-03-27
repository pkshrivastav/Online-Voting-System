from google.cloud import storage

# GCS Configuration
bucket_name = "your-bucket-name"
file_name = "data.json"
gcs_key = "folder/data.json"

# Initialize client
client = storage.Client.from_service_account_json("your-service-account.json")
bucket = client.bucket(bucket_name)
blob = bucket.blob(gcs_key)

# Upload file
blob.upload_from_filename(file_name)

print("File uploaded successfully!")
