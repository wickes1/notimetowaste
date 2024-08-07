import heapq
import string
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st


class Producer:
    def __init__(self, id: int):
        self.id = id
        self.next_production_time: datetime = None


class Consumer:
    def __init__(self, id: str):
        self.id = id
        self.available_time: datetime = None
        self.current_item: Item = None
        self.items_processed: int = 0
        self.total_processing_time: timedelta = timedelta()


class Item:
    def __init__(self, id: int):
        self.id = id
        self.creation_time: datetime = None
        self.processing_start_time: datetime = None
        self.processing_end_time: datetime = None


class EventType(Enum):
    ITEM_PRODUCTION = "item_production"
    PROCESSING_START = "processing_start"
    PROCESSING_END = "processing_end"
    SYSTEM_SHUTDOWN = "system_shutdown"


class Event:
    def __init__(
        self,
        time: datetime,
        event_type: str,
        producer: Producer = None,
        consumer: Consumer = None,
        item: Item = None,
    ):
        self.time: datetime = time
        self.event_type: EventType = event_type
        self.producer: Producer = producer
        self.consumer: Consumer = consumer
        self.item: Item = item

    def __lt__(self, other: "Event") -> bool:
        return self.time < other.time


def get_random_interval(distribution: str, mean: float) -> float:
    if distribution == "exponential":
        return np.random.exponential(mean)
    elif distribution == "poisson":
        return np.random.poisson(mean)
    elif distribution == "uniform":
        return np.random.uniform(0, 2 * mean)
    elif distribution == "fixed":
        return mean
    else:  # default to normal distribution
        return max(0, np.random.normal(mean, mean / 3))


def simulate_system(
    start_time,
    end_time,
    producer_count,
    consumer_names,
    avg_production_interval,
    processing_duration,
    production_distribution="normal",
    processing_distribution="normal",
):
    current_time = start_time
    producers = [Producer(i) for i in range(producer_count)]
    consumers = [Consumer(name) for name in consumer_names]
    waiting_items: List[Item] = []
    item_id = 1
    events: List[Event] = []

    # Statistics
    queue_length_over_time: List[Tuple[datetime, int]] = []
    items_produced = 0
    items_processed = 0
    items_discarded = 0
    total_wait_time: timedelta = timedelta()

    print(f"{current_time.strftime('%H:%M')} System started")

    # Schedule first item production
    for producer in producers:
        production_time = current_time + timedelta(
            seconds=get_random_interval(
                production_distribution, avg_production_interval
            )
        )
        if production_time < end_time:
            heapq.heappush(
                events,
                Event(production_time, EventType.ITEM_PRODUCTION, producer=producer),
            )

    # Schedule system shutdown
    heapq.heappush(events, Event(end_time, EventType.SYSTEM_SHUTDOWN))

    # Collect response time
    response_times = []

    while events:
        event: Event = heapq.heappop(events)
        current_time = event.time

        queue_length_over_time.append((current_time, len(waiting_items)))

        match event.event_type:
            case EventType.ITEM_PRODUCTION:
                if current_time < end_time:
                    item = Item(item_id)
                    item.creation_time = current_time
                    print(f"{current_time.strftime('%H:%M')} Item-{item.id} produced")
                    waiting_items.append(item)
                    item_id += 1
                    items_produced += 1

                    # Schedule next item production for this producer
                    next_production = current_time + timedelta(
                        seconds=get_random_interval(
                            production_distribution, avg_production_interval
                        )
                    )
                    if next_production < end_time:
                        heapq.heappush(
                            events,
                            Event(
                                next_production,
                                EventType.ITEM_PRODUCTION,
                                producer=event.producer,
                            ),
                        )

            case EventType.PROCESSING_END:
                consumer = event.consumer
                item = consumer.current_item
                item.processing_end_time = current_time
                print(
                    f"{current_time.strftime('%H:%M')} {consumer.id} finished processing Item-{item.id}"
                )
                consumer.items_processed += 1
                consumer.total_processing_time += (
                    item.processing_end_time - item.processing_start_time
                )
                consumer.current_item = None
                consumer.available_time = current_time
                items_processed += 1
                response_time = (
                    item.processing_end_time - item.creation_time
                ).total_seconds()  # in seconds
                response_times.append(response_time)

            case EventType.SYSTEM_SHUTDOWN:
                # Handle waiting items at shutdown time
                for item in waiting_items:
                    print(f"{current_time.strftime('%H:%M')} Item-{item.id} discarded")
                    items_discarded += 1
                waiting_items.clear()

        # Assign waiting items to available consumers
        for consumer in consumers:
            if not consumer.current_item and waiting_items and current_time < end_time:
                item = waiting_items.pop(0)
                consumer.current_item = item
                item.processing_start_time = current_time
                total_wait_time += item.processing_start_time - item.creation_time
                process_time = get_random_interval(
                    processing_distribution, processing_duration
                )
                consumer.available_time = current_time + timedelta(seconds=process_time)
                print(
                    f"{current_time.strftime('%H:%M')} {consumer.id} started processing Item-{item.id}"
                )
                heapq.heappush(
                    events,
                    Event(
                        consumer.available_time,
                        EventType.PROCESSING_END,
                        consumer=consumer,
                        item=item,
                    ),
                )

    # Handle consumers finishing up after shutdown time
    while any(consumer.current_item for consumer in consumers):
        consumer = min(
            (c for c in consumers if c.current_item), key=lambda c: c.available_time
        )
        current_time = consumer.available_time
        item = consumer.current_item
        item.processing_end_time = current_time
        print(
            f"{current_time.strftime('%H:%M')} {consumer.id} finished processing Item-{item.id}"
        )
        consumer.items_processed += 1
        consumer.total_processing_time += (
            item.processing_end_time - item.processing_start_time
        )
        consumer.current_item = None
        items_processed += 1

    print(f"{current_time.strftime('%H:%M')} System shut down")

    # Calculate and print statistics
    total_time = (end_time - start_time).total_seconds() / 3600  # in hours
    avg_wait_time = total_wait_time.total_seconds() / items_processed / 60

    response_times = np.array(response_times)
    p90_latency = np.percentile(response_times, 90)
    p95_latency = np.percentile(response_times, 95)
    p99_latency = np.percentile(response_times, 99)
    min_response_time = np.min(response_times)
    max_response_time = np.max(response_times)
    avg_response_time = np.mean(response_times)

    print("System Statistics:")
    print(f"Total items produced: {items_produced}")
    print(f"Total items processed: {items_processed}")
    print(f"Total items discarded: {items_discarded}")
    print(f"Average wait time: {avg_wait_time}")
    print(
        f"System utilization: {sum(c.total_processing_time.total_seconds() for c in consumers) / (len(consumers) * total_time * 3600):.2%}"
    )

    for consumer in consumers:
        print(f"\n{consumer.id} Statistics:")
        print(f"Items processed: {consumer.items_processed}")
        print(
            f"Utilization: {consumer.total_processing_time.total_seconds() / (total_time * 3600):.2%}"
        )

    # Plot queue length over time
    times, queue_lengths = zip(*queue_length_over_time)
    plt.figure(figsize=(12, 6))
    plt.plot(times, queue_lengths)
    plt.title("Queue Length Over Time")
    plt.xlabel("Time")
    plt.ylabel("Queue Length")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Plot consumer utilization
    consumer_names = [c.id for c in consumers]
    utilizations = [
        c.total_processing_time.total_seconds() / (total_time * 3600) for c in consumers
    ]
    plt.figure(figsize=(10, 6))
    plt.bar(consumer_names, utilizations)
    plt.title("Consumer Utilization")
    plt.xlabel("Consumer")
    plt.ylabel("Utilization")
    plt.ylim(0, 1)
    for i, v in enumerate(utilizations):
        plt.text(i, v, f"{v:.2%}", ha="center", va="bottom")
    plt.tight_layout()

    # Create latency distribution chart
    fig_latency, ax_latency = plt.subplots(figsize=(10, 6))
    sns.histplot(response_times, kde=True, ax=ax_latency)
    ax_latency.set_title("Latency Distribution")
    ax_latency.set_xlabel("Response Time (seconds)")
    ax_latency.set_ylabel("Frequency")

    # Create and return figures instead of showing them
    fig_queue, ax_queue = plt.subplots(figsize=(12, 6))
    ax_queue.plot(times, queue_lengths)
    ax_queue.set_title("Queue Length Over Time")
    ax_queue.set_xlabel("Time")
    ax_queue.set_ylabel("Queue Length")
    plt.xticks(rotation=45)

    fig_util, ax_util = plt.subplots(figsize=(10, 6))
    ax_util.bar(consumer_names, utilizations)
    ax_util.set_title("Consumer Utilization")
    ax_util.set_xlabel("Consumer")
    ax_util.set_ylabel("Utilization")
    ax_util.set_ylim(0, 1)
    for i, v in enumerate(utilizations):
        ax_util.text(i, v, f"{v:.2%}", ha="center", va="bottom")

    return {
        "stats": {
            "Total items produced": items_produced,
            "Total items processed": items_processed,
            "Total items discarded": items_discarded,
            "Average wait time": f"{avg_wait_time * 60:.2f} seconds",
            "System utilization": f"{sum(c.total_processing_time.total_seconds() for c in consumers) / (len(consumers) * total_time * 3600):.2%}",
            "P90 Latency": f"{p90_latency:.2f} seconds",
            "P95 Latency": f"{p95_latency:.2f} seconds",
            "P99 Latency": f"{p99_latency:.2f} seconds",
            "Min Response Time": f"{min_response_time:.2f} seconds",
            "Max Response Time": f"{max_response_time:.2f} seconds",
            "Avg Response Time": f"{avg_response_time:.2f} seconds",
        },
        "consumer_stats": [
            {
                "Consumer": consumer.id,
                "Items processed": consumer.items_processed,
                "Utilization": f"{consumer.total_processing_time.total_seconds() / (total_time * 3600):.2%}",
            }
            for consumer in consumers
        ],
        "figures": {
            "queue_length": fig_queue,
            "consumer_utilization": fig_util,
            "latency_distribution": fig_latency,
        },
    }


# Streamlit app
st.title("Queueing System Simulation")

# Sidebar for user inputs
st.sidebar.header("Simulation Configuration")

start_date = st.sidebar.date_input("Start Date", datetime(2024, 1, 1).date())
start_time = st.sidebar.time_input("Start Time", datetime(2024, 1, 1, 0, 0).time())
end_date = st.sidebar.date_input("End Date", datetime(2024, 1, 1).date())
end_time = st.sidebar.time_input("End Time", datetime(2024, 1, 1, 6, 0).time())

st.sidebar.subheader("System Parameters")
producer_count = st.sidebar.number_input("Number of Producers", min_value=1, value=2)
consumer_count = st.sidebar.number_input("Number of Consumers", min_value=1, value=4)
avg_production_interval = st.sidebar.number_input(
    "Average Production Interval (seconds)", min_value=1, value=1
)
processing_duration = st.sidebar.number_input(
    "Processing Duration (seconds)", min_value=1, value=2
)

st.sidebar.subheader("Distribution Settings")
production_distribution = st.sidebar.selectbox(
    "Production Distribution", ["poisson", "exponential", "uniform", "fixed", "normal"]
)
processing_distribution = st.sidebar.selectbox(
    "Processing Distribution", ["fixed", "exponential", "uniform", "poisson", "normal"]
)

if st.sidebar.button("Run Simulation"):
    start_datetime = datetime.combine(start_date, start_time)
    end_datetime = datetime.combine(end_date, end_time)
    consumer_names = [
        f"Consumer-{letter}" for letter in string.ascii_uppercase[:consumer_count]
    ]

    results = simulate_system(
        start_datetime,
        end_datetime,
        producer_count,
        consumer_names,
        avg_production_interval,
        processing_duration,
        production_distribution,
        processing_distribution,
    )

    # Display results in the main area
    st.subheader("System Statistics")
    st.write(pd.DataFrame([results["stats"]]).T)

    st.subheader("Consumer Statistics")
    st.write(pd.DataFrame(results["consumer_stats"]))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Queue Length Over Time")
        st.pyplot(results["figures"]["queue_length"])

    with col2:
        st.subheader("Consumer Utilization")
        st.pyplot(results["figures"]["consumer_utilization"])

    st.subheader("Latency Distribution")
    st.pyplot(results["figures"]["latency_distribution"])

else:
    st.write(
        "Configure the simulation parameters in the sidebar and click 'Run Simulation' to see the results."
    )
