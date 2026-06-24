import asyncio
import pyarrow.parquet as pq
from simulator import RideSimulator
from pipeline import StreamingFeatureEngine
from model import SurgePricingModel

DATA_PATH = "data/raw/yellow_tripdata_2023-01.parquet"

async def main():
    print("--- Starting Dynamic Pricing Engine ---")
    
    # 1. Initialize Components
    simulator = RideSimulator(DATA_PATH, batch_size=50)
    pipeline = StreamingFeatureEngine(window_seconds=600)
    model = SurgePricingModel()
    
    # 2. Execute Warm Start (Extract first 10,000 rows to train baseline)
    print("Loading historical data for warm start...")
    parquet_file = pq.ParquetFile(DATA_PATH)
    warmup_batch = next(parquet_file.iter_batches(batch_size=10000)).to_pandas()
    warmup_batch = warmup_batch[warmup_batch['fare_amount'] > 0]
    
    warmup_features, warmup_targets = pipeline.process_batch(warmup_batch)
    model.warm_start(warmup_features, warmup_targets)
    
    # 3. Live Streaming Loop
    print("\n--- Listening to Live Ride Stream ---")
    batch_count = 0
    
    async for raw_batch in simulator.stream_requests():
        # Feature Engineering Window
        features, _ = pipeline.process_batch(raw_batch)
        
        # GPU Inference
        dynamic_prices = model.predict_surge(features)
        
        # Construct Console Output
        results = features.copy()
        results['dynamic_price'] = dynamic_prices
        
        batch_count += 1
        if batch_count % 10 == 0:
            print(f"Processed Batch {batch_count} | Sample Output:")
            print(results[['pickup_location', 'local_10min_demand', 'dynamic_price']].head(3))
            print("-" * 40)

if __name__ == "__main__":
    asyncio.run(main())