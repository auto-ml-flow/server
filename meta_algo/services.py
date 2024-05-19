import csv
from django.db.models import Avg, Sum

from experiment.models import RunModel
from system.models import CPUStatsModel, DiskStatsModel, MemoryStatsModel, NetworkStatsModel

def get_successful_run_stats():
    successful_runs = RunModel.objects.filter(status=RunModel.DONE)
    run_stats = []
    print(successful_runs)

    for run in successful_runs:
        system = run.systemmodel
        memory_stats = MemoryStatsModel.objects.filter(system=system).aggregate(
            avg_usage_megabytes=Avg('usage_megabytes'),
            avg_usage_percentage=Avg('usage_percentage')
        )
        cpu_stats = CPUStatsModel.objects.filter(system=system).aggregate(
            avg_utilization=Avg('utilization')
        )
        disk_stats = DiskStatsModel.objects.filter(system=system).aggregate(
            avg_usage_percentage=Avg('usage_percentage'),
            avg_usage_megabytes=Avg('usage_megabytes'),
            avg_available=Avg('available')
        )
        network_stats = NetworkStatsModel.objects.filter(system=system).aggregate(
            sum_receive_megabytes=Sum('receive_megabytes'),
            sum_transmit_megabytes=Sum('transmit_megabytes')
        )

        run_stat = {
            'system_ram': system.ram,
            'system_swap': system.swap,
            'system_swap_available': system.swap_available,
            'system_load_avg_last_min': system.load_avg_last_min,
            'system_load_avg_last_5_min': system.load_avg_last_5_min,
            'system_load_avg_last_15_min': system.load_avg_last_15_min,
            'dataset_n_features': run.dataset.n_features,
            'dataset_n_samples': run.dataset.n_samples,
            'avg_memory_usage_megabytes': memory_stats['avg_usage_megabytes'],
            'avg_memory_usage_percentage': memory_stats['avg_usage_percentage'],
            'avg_cpu_utilization': cpu_stats['avg_utilization'],
            'avg_disk_usage_percentage': disk_stats['avg_usage_percentage'],
            'avg_disk_usage_megabytes': disk_stats['avg_usage_megabytes'],
            'avg_disk_available': disk_stats['avg_available'],
            'sum_network_receive_megabytes': network_stats['sum_receive_megabytes'],
            'sum_network_transmit_megabytes': network_stats['sum_transmit_megabytes'],
            'duration': run.duration,
        }

        run_stats.append(run_stat)

    return run_stats

def save_run_stats_to_csv(run_stats, filename):
    fieldnames = [
        'system_ram', 'system_swap', 'system_swap_available', 'system_load_avg_last_min',
        'system_load_avg_last_5_min', 'system_load_avg_last_15_min', 'dataset_n_features',
        'dataset_n_samples', 'avg_memory_usage_megabytes', 'avg_memory_usage_percentage',
        'avg_cpu_utilization', 'avg_disk_usage_percentage', 'avg_disk_usage_megabytes',
        'avg_disk_available', 'sum_network_receive_megabytes', 'sum_network_transmit_megabytes',
        'duration'
    ]

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(run_stats)

def test():
    import pandas as pd

    df = pd.read_csv('run_stats.csv', sep='\t')

    print(df.head())
    features = [
        'system_ram', 'system_swap', 'system_swap_available', 'system_load_avg_last_min',
        'system_load_avg_last_5_min', 'system_load_avg_last_15_min', 'dataset_n_features',
        'dataset_n_samples', 'avg_memory_usage_megabytes', 'avg_memory_usage_percentage',
        'avg_cpu_utilization', 'avg_disk_usage_percentage', 'avg_disk_usage_megabytes',
        'avg_disk_available', 'sum_network_receive_megabytes', 'sum_network_transmit_megabytes',
    ]
    target = 'duration'

    df[features].describe()
    from lazypredict.Supervised import LazyRegressor
    from sklearn.utils import shuffle
    import numpy as np

    X, y = shuffle(df[features], df[target], random_state=13)
    X = X.astype(np.float32)

    offset = int(X.shape[0] * 0.9)

    X_train, y_train = X[:offset], y[:offset]
    X_test, y_test = X[offset:], y[offset:]

    reg = LazyRegressor(verbose=0, ignore_warnings=False, custom_metric=None)
    models, predictions = reg.fit(X_train, X_test, y_train, y_test)
    print(models)
    
    import numpy as np
    from sklearn.svm import SVR
    from sklearn.model_selection import GridSearchCV
    from sklearn.metrics import mean_squared_error

    param_grid = {
        "C": [0.1, 1, 10, 100],
        "gamma": [1, 0.1, 0.01, 0.001],
        "epsilon": [0.1, 0.01, 0.001],
    }

    reg = SVR()

    grid_search = GridSearchCV(reg, param_grid, cv=5, scoring='neg_mean_squared_error', return_train_score=True)
    grid_search.fit(X_train, y_train)

    print("Best hyperparameters: ", grid_search.best_params_)

    print("Best score: ", -grid_search.best_score_)

    reg_best = SVR(**grid_search.best_params_)
    reg_best.fit(X_train, y_train)

    y_pred = reg_best.predict(X_test)

    rmse = mean_squared_error(y_test, y_pred, squared=False)
    mse = mean_squared_error(y_test, y_pred)
    max_error = np.max(np.abs(y_test - y_pred))
    min_error = np.min(np.abs(y_test - y_pred))
    print("RMSE: ", rmse)
    print("MSE: ", mse)
    print("Max Error: ", max_error)
    print("Min Error: ", min_error)

# Usage example
# run_stats = get_successful_run_stats()
# save_run_stats_to_csv(run_stats, 'run_stats.csv')