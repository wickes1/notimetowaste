import time

import pyspark.sql.functions as F
from pyspark.sql import SparkSession

from common import create_spark_session


def analyze_data(spark: SparkSession):
    data = spark.read.parquet("/opt/spark-data/*.parquet").repartition(4)

    print(f"The data contains: {data.count()} rows")

    agg_by_pickup_location = (
        data.groupBy("PULocationID")
        .agg(
            F.count(F.lit(1)).alias("num_rows"),
            F.avg("Tip_amount").alias("avg_tip"),
        )
        .filter(F.col("num_rows") > 20)
    )

    agg_by_pickup_location.sort(F.col("avg_tip").desc()).show(truncate=False, n=10)
    agg_by_pickup_location.write.option("header", "true").mode("overwrite").csv(
        f"/opt/spark-data/agg_by_pickup_location_{int(time.time())}.csv"
    )


if __name__ == "__main__":
    spark = create_spark_session("Analyze Taxi Data")
    analyze_data(spark)

    # Uncomment the following lines to keep the spark session open
    # input("Press enter to terminate spark session...")
    # spark.stop()
