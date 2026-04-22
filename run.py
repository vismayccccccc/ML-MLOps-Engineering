import argparse
import pandas as pd
import yaml
import numpy as np
import logging
import json
import time
import sys


def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def load_config(config_path):
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        required_keys = ["seed", "window", "version"]
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing config key: {key}")

        np.random.seed(config["seed"])
        logging.info(f"Config loaded: {config}")

        return config

    except Exception as e:
        logging.error(str(e))
        raise


def load_data(input_path):
    try:
        df = pd.read_csv(input_path)

        if df.empty:
            raise ValueError("Empty dataset")

        if "close" not in df.columns:
            raise ValueError("Missing close column")

        logging.info(f"Rows loaded: {len(df)}")
        return df

    except Exception as e:
        logging.error(str(e))
        raise


def process_data(df, window):
    try:
        df["rolling_mean"] = df["close"].rolling(window=window).mean()

        df["signal"] = np.where(df["close"] > df["rolling_mean"], 1, 0)

        signal_rate = df["signal"].mean()

        logging.info("Rolling mean computed")
        logging.info("Signal generation completed")

        return df, signal_rate

    except Exception as e:
        logging.error(str(e))
        raise


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)

    args = parser.parse_args()

    setup_logging(args.log_file)

    start_time = time.time()

    try:
        logging.info("Job started")

        config = load_config(args.config)
        df = load_data(args.input)

        df, signal_rate = process_data(df, config["window"])

        latency_ms = int((time.time() - start_time) * 1000)

        metrics = {
            "version": config["version"],
            "rows_processed": len(df),
            "metric": "signal_rate",
            "value": float(signal_rate),
            "latency_ms": latency_ms,
            "seed": config["seed"],
            "status": "success"
        }

        with open(args.output, "w") as f:
            json.dump(metrics, f, indent=4)

        logging.info(f"Metrics: {metrics}")
        logging.info("Job completed successfully")

        print(json.dumps(metrics))

    except Exception as e:

        error_output = {
            "version": "v1",
            "status": "error",
            "error_message": str(e)
        }

        with open(args.output, "w") as f:
            json.dump(error_output, f, indent=4)

        logging.error(str(e))

        print(json.dumps(error_output))
        sys.exit(1)


if __name__ == "__main__":
    main()
