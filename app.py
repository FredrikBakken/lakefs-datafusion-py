import os
import datafusion

from datafusion.object_store import AmazonS3
from dotenv import load_dotenv


load_dotenv()

region = "us-east-1"
repo = "demo"
branch = "main"

s3a = AmazonS3(
    bucket_name=repo,
    region=region,
    access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    endpoint="http://localhost:8000",
    allow_http=True,
)

ctx = datafusion.SessionContext()
path = f"s3a://{repo}/{branch}/taxi_data/input/yellow_tripdata_2022-02.parquet"
ctx.register_object_store(path, s3a)

ctx.register_parquet("taxi_table", path)

df = ctx.sql("SELECT * FROM taxi_table")

out_path = f"s3a://{repo}/{branch}/taxi_data/output/parquet-py/"
df.write_parquet(out_path)

json_path = f"s3a://{repo}/{branch}/taxi_data/output/json-py"
df.write_json(json_path)

csv_path = f"s3a://{repo}/{branch}/taxi_data/output/csv-py"
df.write_csv(csv_path)

df.show()
