import csv
import io
import logging
import pickle
from datetime import datetime
from typing import Literal

import numpy as np
import pandas as pd
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
from sklearn.utils import shuffle
from xgboost import XGBRegressor

from auto_ml_flow.celery_app import app
from meta_algo.models import MetaAlgoModel, PreparedDatasetModel
from meta_algo.services import get_successful_run_stats

logger = logging.getLogger(__name__)


@app.task()
def create_prepared_dataset(target: str = "duration") -> None:
    stats = get_successful_run_stats()
    if not stats:
        logger.info("No stats available. Skipping dataset creation.")
        return

    labels = list(stats[0].keys())  # Get keys as labels

    # Generate a unique filename with the current timestamp
    filename = f"{target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    try:
        # Use StringIO to create an in-memory file-like object
        csv_data = io.StringIO()
        writer = csv.DictWriter(csv_data, fieldnames=labels)
        writer.writeheader()
        writer.writerows(stats)
        csv_data.seek(0)  # Move to the start of the StringIO object to read its content later

        # Convert the StringIO object to an InMemoryUploadedFile
        csv_file = InMemoryUploadedFile(
            csv_data,  # file
            None,  # field name, not required here
            filename,  # file name
            "text/csv",  # content type
            csv_data.tell(),  # size
            None,  # charset, not needed
        )

        # Create the model instance with the in-memory file
        PreparedDatasetModel.objects.create(labels=labels, target=target, csv_file=csv_file)
    except Exception as e:
        logger.error(f"Error creating PreparedDatasetModel: {e}")
    print("a")


@app.task()
def fit_meta_algo(target: Literal["DURATION", "PREDICT"] = "DURATION") -> None:
    print("b")
    try:
        prepared_dataset = PreparedDatasetModel.objects.latest("created_at")
        csv_file = prepared_dataset.csv_file

        # Read the content of the csv file into a pandas DataFrame
        csv_data = csv_file.read().decode("utf-8")  # Read and decode the content to a string
        df = pd.read_csv(
            io.StringIO(csv_data)
        )  # Use StringIO to convert the string to a file-like object
    except Exception as e:
        logger.error(f"Error reading dataset in fit_meta_algo: {e}")
        return

    if len(df) < 10:
        logger.error("Too less data for learning")
        return

    X, y = shuffle(df[prepared_dataset.labels], df[prepared_dataset.target], random_state=42)
    X = X.astype(np.float32)

    offset = int(X.shape[0] * 0.9)

    X_train, y_train = X[:offset], y[:offset]
    X_test, y_test = X[offset:], y[offset:]

    param_grid = {
        "n_estimators": [200, 300],
        "max_depth": [3, 4, 5],
        "learning_rate": [0.01, 0.1],
        "subsample": [0.8, 0.9],
        "colsample_bytree": [0.8, 0.9],
        "gamma": [0, 0.1],
    }

    reg = XGBRegressor()

    grid_search = GridSearchCV(
        reg, param_grid, cv=5, scoring="neg_mean_squared_error", return_train_score=True
    )
    grid_search.fit(X_train, y_train)

    logger.info(f"Best hyperparameters: {grid_search.best_params_}")

    logger.info(f"Best score: {-grid_search.best_score_}")

    reg_best = XGBRegressor(**grid_search.best_params_)
    reg_best.fit(X_train, y_train)

    y_pred = reg_best.predict(X_test)

    rmse = mean_squared_error(y_test, y_pred, squared=False)
    mse = mean_squared_error(y_test, y_pred)
    max_error = np.max(np.abs(y_test - y_pred))
    min_error = np.min(np.abs(y_test - y_pred))

    logger.info(f"RMSE: {rmse}")
    logger.info(f"MSE: {mse}")
    logger.info(f"Max Error: {max_error}")
    logger.info(f"Min Error: { min_error}")

    type_ = MetaAlgoModel.PREDICT if target == MetaAlgoModel.PREDICT else MetaAlgoModel.DURATION

    try:
        # Serialize the model to a file-like object using pickle
        model_file = io.BytesIO()
        pickle.dump(reg_best, model_file)
        model_file.seek(0)  # Move to the start of the BytesIO object

        # Create a new MetaAlgoModel instance and save it to the database
        MetaAlgoModel.objects.create(
            type=type_,
            mse=mse,
            rmse=rmse,
            max_error=max_error,
            min_error=min_error,
            model=ContentFile(
                model_file.read(), name=f"meta_algo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
            ),
            dataset=prepared_dataset,
        )
    except Exception as e:
        logger.error(f"Error saving model to MetaAlgoModel: {e}")

    print("c")
