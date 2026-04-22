# ML-MLOps-Engineering
TThis project is a lightweight MLOps batch processing pipeline built using Python. It demonstrates key production-level ML engineering concepts such as reproducibility, observability, and deployment readiness.

The pipeline processes OHLCV (Open, High, Low, Close, Volume) financial data from a CSV file, computes a rolling mean on the closing price, and generates a binary trading signal based on whether the close price is above or below the rolling average.

The system is fully configurable using a YAML configuration file and supports CLI-based execution for automation and reproducibility.

FEATURES:
YAML-based configuration (seed, window, version)
CSV data ingestion and validation
Rolling mean feature engineering
Binary signal generation (1/0)
Structured logging for observability
Metrics output in JSON format
CLI-based execution
Error handling and validation
