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
    # Функция для создания подготовленного набора данных
    # target - целевая переменная, по умолчанию "duration"

    stats = get_successful_run_stats()
    # Получение статистики об успешных запусках

    if not stats:
    # Если статистика недоступна, то выводим сообщение и прерываем выполнение функции
        logger.info("No stats available. Skipping dataset creation.")
        return

    labels = list(stats[0].keys())
    # Получение ключей в виде списка для использования в качестве меток

    filename = f"{target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    # Генерация уникального имени файла с использованием текущей временной метки

    try:
    # Блок кода, выполнение которого может привести к возникновению исключения
        # Use StringIO to create an in-memory file-like object
        csv_data = io.StringIO()
        # Создание в памяти объекта, подобного файлу, с использованием StringIO

        writer = csv.DictWriter(csv_data, fieldnames=labels)
        # Создание объекта-записывателя csv-файла с использованием меток в качестве имен полей

        writer.writeheader()
        # Запись заголовка в csv-файл

        writer.writerows(stats)
        # Запись статистики в csv-файл

        csv_data.seek(0)
        # Перемещение указателя в начало csv-файла для последующего чтения

        # Convert the StringIO object to an InMemoryUploadedFile
        csv_file = InMemoryUploadedFile(
            csv_data,
            # file - файл
            None,
            # field name - имя поля, не требуется здесь
            filename,
            # file name - имя файла
            "text/csv",
            # content type - тип содержимого
            csv_data.tell(),
            # size - размер
            None,
            # charset - кодировка, не требуется здесь
        )
        # Преобразование объекта StringIO в объект InMemoryUploadedFile

        # Create the model instance with the in-memory file
        PreparedDatasetModel.objects.create(labels=labels, target=target, csv_file=csv_file)
        # Создание экземпляра модели с использованием меток, целевой переменной и csv-файла в памяти
    except Exception as e:
    # Блок кода, выполняемый при возникновении исключения
        logger.error(f"Error creating PreparedDatasetModel: {e}")
        # Вывод сообщения об ошибке при создании экземпляра модели



@app.task()
def fit_meta_algo(target: Literal["DURATION", "PREDICT"] = "DURATION") -> None:
    # Функция для обучения мета-алгоритма с использованием целевой переменной target

    try:
    # Блок кода, выполнение которого может привести к возникновению исключения
        prepared_dataset = PreparedDatasetModel.objects.latest("created_at")
        # Получение последнего созданного набора данных

        csv_file = prepared_dataset.csv_file
        # Получение csv-файла из набора данных

        # Read the content of the csv file into a pandas DataFrame
        csv_data = csv_file.read().decode("utf-8")
        # Чтение и декодирование содержимого csv-файла в строку

        df = pd.read_csv(
            io.StringIO(csv_data)
        )
        # Чтение csv-файла из строки в DataFrame с использованием StringIO

    except Exception as e:
    # Блок кода, выполняемый при возникновении исключения
        logger.error(f"Error reading dataset in fit_meta_algo: {e}")
        # Вывод сообщения об ошибке при чтении набора данных
        return
        # Прерывание выполнения функции

    if len(df) < 10:
    # Если количество строк в DataFrame меньше 10, то:
        logger.error("Too less data for learning")
        # Вывод сообщения об ошибке при недостаточном количестве данных для обучения
        return
        # Прерывание выполнения функции

    X, y = shuffle(df[prepared_dataset.labels], df[prepared_dataset.target], random_state=42)
    # Разделение DataFrame на признаки X и целевую переменную y с использованием шуффлирования

    X = X.astype(np.float32)
    # Преобразование типа данных признаков X в float32

    offset = int(X.shape[0] * 0.9)
    # Вычисление индекса, разделяющего данные на обучающую и тестовую выборки (90% на обучение, 10% на тест)

    X_train, y_train = X[:offset], y[:offset]
    # Получение обучающей выборки

    X_test, y_test = X[offset:], y[offset:]
    # Получение тестовой выборки

    param_grid = {
    # Словарь с гиперпараметрами для поиска лучших значений с использованием GridSearchCV
        "n_estimators": [200, 300],
        "max_depth": [3, 4, 5],
        "learning_rate": [0.01, 0.1],
        "subsample": [0.8, 0.9],
        "colsample_bytree": [0.8, 0.9],
        "gamma": [0, 0.1],
    }

    reg = XGBRegressor()
    # Создание объекта-регрессора XGBoost

    grid_search = GridSearchCV(
    # Создание объекта GridSearchCV для поиска лучших гиперпараметров
        reg, param_grid, cv=5, scoring="neg_mean_squared_error", return_train_score=True
    )

    grid_search.fit(X_train, y_train)
    # Обучение объекта GridSearchCV на обучающей выборке

    logger.info(f"Best hyperparameters: {grid_search.best_params_}")
    # Вывод в лог лучших гиперпараметров

    logger.info(f"Best score: {-grid_search.best_score_}")
    # Вывод в лог лучшего значения метрики (отрицательное, т.к. GridSearchCV минимизирует метрику)

    reg_best = XGBRegressor(**grid_search.best_params_)
    # Создание объекта-регрессора XGBoost с использованием лучших гиперпараметров

    reg_best.fit(X_train, y_train)
    # Обучение объекта-регрессора XGBoost на обучающей выборке

    y_pred = reg_best.predict(X_test)
    # Предсказание значений целевой переменной на тестовой выборке

    rmse = mean_squared_error(y_test, y_pred, squared=False)
    # Вычисление RMSE

    mse = mean_squared_error(y_test, y_pred)
    # Вычисление MSE

    max_error = np.max(np.abs(y_test - y_pred))
    # Вычисление максимальной абсолютной ошибки

    min_error = np.min(np.abs(y_test - y_pred))
    # Вычисление минимальной абсолютной ошибки

    logger.info(f"RMSE: {rmse}")
    # Вывод в лог RMSE

    logger.info(f"MSE: {mse}")
    # Вывод в лог MSE

    logger.info(f"Max Error: {max_error}")
    # Вывод в лог максимальной абсолютной ошибки

    logger.info(f"Min Error: { min_error}")
    # Вывод в лог минимальной абсолютной ошибки

    type_ = MetaAlgoModel.PREDICT if target == MetaAlgoModel.PREDICT else MetaAlgoModel.DURATION
    # Определение типа модели в зависимости от целевой переменной target

    try:
    # Блок кода, выполнение которого может привести к возникновению исключения
        # Serialize the model to a file-like object using pickle
        model_file = io.BytesIO()
        # Создание в памяти объекта, подобного файлу, с использованием BytesIO

        pickle.dump(reg_best, model_file)
        # Сериализация объекта-регрессора XGBoost с использованием pickle

        model_file.seek(0)
        # Перемещение указателя в начало объекта BytesIO для последующего чтения

        # Create a new MetaAlgoModel instance and save it to the database
        MetaAlgoModel.objects.create(
        # Создание экземпляра модели MetaAlgoModel и сохранение его в базе данных
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
    # Блок кода, выполняемый при возникновении исключения
        logger.error(f"Error saving model to MetaAlgoModel: {e}")
        # Вывод сообщения об ошибке при сохранении модели в базе данных

