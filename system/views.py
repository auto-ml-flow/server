from django.views import generic

from system.models import SystemModel


class SystemListView(generic.ListView):
    template_name = "system/list.html"
    queryset = SystemModel.objects.order_by("-created_at")
    paginate_by = 10
    context_object_name = "systems"


from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext as _
from system.models import MemoryStatsModel, CPUStatsModel, DiskStatsModel, NetworkStatsModel
import pandas as pd
from django.db.models import Avg

def aggregate_statistics(statistics, date_field='created_at', segments=20):
    if statistics.count() == 0:
        return []
    
    # Convert QuerySet to DataFrame
    df = pd.DataFrame.from_records(statistics.values())
    
    # Ensure the date_field is a datetime type
    df[date_field] = pd.to_datetime(df[date_field])
    
    # Sort by date
    df.sort_values(by=date_field, inplace=True)
    
    # Calculate resampling frequency
    num_records = len(df)
    if num_records < segments:
        segments = num_records
    
    resample_frequency = f'{max(1, num_records // segments)}T'
    
    # Resample to reduce to `segments` number of data points
    resampled_df = df.set_index(date_field).resample(resample_frequency).mean().dropna()
    
    # Convert back to dictionary format
    return resampled_df.reset_index().to_dict('records')


def system_detail_view(request, pk):
    system = get_object_or_404(SystemModel, pk=pk)
    
    # Aggregate data
    system_statistics = aggregate_statistics(MemoryStatsModel.objects.filter(system=system))
    cpu_statistics = aggregate_statistics(CPUStatsModel.objects.filter(system=system))
    disk_statistics = aggregate_statistics(DiskStatsModel.objects.filter(system=system))
    network_statistics = aggregate_statistics(NetworkStatsModel.objects.filter(system=system))
    
    context = {
        'system': system,
        'system_statistics': system_statistics,
        'cpu_statistics': cpu_statistics,
        'disk_statistics': disk_statistics,
        'network_statistics': network_statistics,
    }
    
    return render(request, 'system/detail.html', context)
