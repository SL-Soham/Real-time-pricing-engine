import pyarrow.parquet as pq
import asyncio

class RideSimulator:
    def __init__(self, file_path: str, batch_size: int = 50):
        self.file_path = file_path
        self.batch_size = batch_size

    async def stream_requests(self):
        """Yields micro-batches of ride requests to simulate live traffic."""
        parquet_file = pq.ParquetFile(self.file_path)
        
        # Iterate over row groups memory-efficiently
        for batch in parquet_file.iter_batches(batch_size=self.batch_size):
            df_batch = batch.to_pandas()
            
            # Simulate real-time API delay between batches
            await asyncio.sleep(0.1) 
            
            # Clean anomalous data (e.g., negative fares)
            df_batch = df_batch[df_batch['fare_amount'] > 0]
            
            if not df_batch.empty:
                yield df_batch