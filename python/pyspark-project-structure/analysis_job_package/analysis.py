import pandas as pd
import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql import DataFrame
from pyspark.sql.pandas.functions import pandas_udf


@pandas_udf(returnType=T.IntegerType())
def trip_duration(start_time: pd.Series, end_time: pd.Series) -> pd.Series:
    return (end_time - start_time).dt.seconds


def calculate_avg_trip_duration(trips_data: DataFrame):
    result_data = (
        trips_data.withColumn(
            "duration",
            trip_duration(
                F.col("lpep_pickup_datetime"), F.col("lpep_dropoff_datetime")
            ),
        )
        .groupby("VendorID")
        .agg(F.avg(F.col("duration")).alias("avg_duration"))
    )

    return result_data
