import xgboost as xgb
import pandas as pd
from sklearn.model_selection import train_test_split

class SurgePricingModel:
    def __init__(self):
        # Configure strictly for the MX570A (2GB VRAM limit)
        # Using a shallow depth and small memory footprint
        self.params = {
            'objective': 'reg:squarederror',
            'device': 'cuda',          # Hardware acceleration on MX570A
            'tree_method': 'hist',     # Required for CUDA
            'max_depth': 4,            # Kept small to fit in 2GB VRAM
            'learning_rate': 0.1,
            'verbosity': 0
        }
        self.model = None

    def warm_start(self, features: pd.DataFrame, targets: pd.Series):
        """Train baseline intelligence on an initial historical batch."""
        print("[GPU] Initiating Warm Start on MX570A...")
        X_train, X_val, y_train, y_val = train_test_split(features, targets, test_size=0.2)
        
        # Load data into DMatrix (efficient XGBoost format)
        dtrain = xgb.DMatrix(X_train, label=y_train)
        dval = xgb.DMatrix(X_val, label=y_val)
        
        self.model = xgb.train(
            self.params,
            dtrain,
            num_boost_round=100,
            evals=[(dval, 'validation')],
            early_stopping_rounds=10,
            verbose_eval=False
        )
        print("[GPU] Warm Start Complete. Model loaded in VRAM.")

    def predict_surge(self, features: pd.DataFrame) -> pd.DataFrame:
        """Run real-time inference on the streaming micro-batch."""
        if not self.model:
            raise ValueError("Model must be warm-started before inference.")
        
        dtest = xgb.DMatrix(features)
        base_fares = self.model.predict(dtest)
        
        # Simple dynamic pricing logic: Base fare + Surge multiplier based on demand
        demand_multiplier = 1 + (features['local_10min_demand'] * 0.05)
        dynamic_prices = base_fares * demand_multiplier
        
        return dynamic_prices