# Pyspark Project Structure

## Pyspark project workflow

```bash
# Create virtual environment
python -m venv venv --prompt pyspark-project-structure
source venv/bin/activate

# Install dependencies
echo "pyspark==3.5.0" > requirements.txt
pip install --upgrade pip && pip install -r requirements.txt
```

## Data download

```bash
# Download data
mkdir data

# Download data
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-09.parquet -P data
wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2023-09.parquet -P data

```

## Packaging and Executing on a Spark cluster

In cluster mode, the driver runs on a cluster, while in client mode, the driver runs on the local machine.

- short-lived (ephemeral) clusters usually appropriate to install the required libraries on cluster nodes
- shared clusters, it is better to package the application and submit it to the cluster

## Docker Spark Cluster

```bash
docker build -t spark-docker-image-3.5.0:latest .
docker compose up
```

## Commit Job to Spark Cluster

```bash
# Put the package file (common.py) in job_package folder and zip it and copy to cluster apps folder
mkdir job_package && cp common.py job_package/common.py && zip -r -j job_zip.zip job_package/*.py
rm -r job_package
cp ./job_zip.zip docker-spark/apps

# Copy job file (job.py) to cluster apps folder
cp ./job.py docker-spark/apps

# Copy data to cluster data folder
cp -r ./data docker-spark/data

# Connect to the master node
docker exec -it docker-spark-spark-master-1 /bin/bash

# Check master URL from the Spark UI, localhost:9000
# Submit the job
/opt/spark/bin/spark-submit --master <master URL> --py-files /opt/spark-apps/job_zip.zip /opt/spark-apps/job.py

```

## Commit Job with Dependencies to Spark Cluster

```bash
# Set up the environment
export PYSPARK_PYTHON=/opt/spark/environment/bin/python


# Commit the job with specify the environment and python packages
# Visit http://localhost:9000 to get the master URL
# Visit http://localhost:4040 to view the job status
/opt/spark/bin/spark-submit \
--master <master URL> \
--archives /opt/spark-apps/job_dependencies.tar.gz#environment \
--py-files /opt/spark-apps/analysis_job_zip.zip /opt/spark-apps/second_job.py
```

## Workflow Diagram

![https://miro.medium.com/v2/resize:fit:2000/format:webp/1*iGhmRmhHkejytMl2ffiiLw.png](https://miro.medium.com/v2/resize:fit:2000/format:webp/1*iGhmRmhHkejytMl2ffiiLw.png)

## FAQ

### Error:'java.lang.UnsupportedOperationException' for Pyspark pandas_udf documentation code

```bash
sudo archlinux-java set java-8-openjdk
```

## References

[Spark Essentials: A Guide to Setting Up, Packaging, and Running PySpark Projects](https://medium.com/@suffyan.asad1/spark-essentials-a-guide-to-setting-up-packaging-and-running-pyspark-projects-2eb2a27523a3)
