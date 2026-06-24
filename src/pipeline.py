import pandas as pd
from collections import deque, defaultdict
import time

class StreamingFeatureEngine:
    def __init__(self, window_seconds: int = 600):
        self.window_seconds = window_seconds
        # Dictionary mapping PULocationID to a deque of timestamps
        self.demand_spikes = defaultdict(deque)

    def process_batch(self, batch_df: pd.DataFrame) -> pd.DataFrame:
        """Computes rolling features for the current batch."""
        current_time = time.time()
        cutoff_time = current_time - self.window_seconds
        
        demand_features = []
        
        for _, row in batch_df.iterrows():
            loc_id = row['PULocationID']
            
            # 1. Update the sliding window for this location
            self.demand_spikes[loc_id].append(current_time)
            
            # 2. Evict expired requests (older than 10 minutes)
            while self.demand_spikes[loc_id] and self.demand_spikes[loc_id][0] < cutoff_time:
                self.demand_spikes[loc_id].popleft()
            
            # 3. Compute local cluster demand (number of requests in the window)
            current_demand = len(self.demand_spikes[loc_id])
            demand_features.append(current_demand)
            
        # Engineer the final feature set for the model
        features_df = pd.DataFrame({
            'trip_distance': batch_df['trip_distance'],
            'pickup_location': batch_df['PULocationID'],
            'dropoff_location': batch_df['DOLocationID'],
            'passenger_count': batch_df['passenger_count'].fillna(1),
            'local_10min_demand': demand_features
        })
        
        return features_df, batch_df['fare_amount']