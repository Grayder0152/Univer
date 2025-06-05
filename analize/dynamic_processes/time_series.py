from dataclasses import dataclass
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


@dataclass
class TimeSeries:
    file_path: str
    series_col_name: str
    time_col_name: str
    time_format: str
    dataset: Optional[pd.DataFrame] = None

    def __post_init__(self):
        self.dataset = self._load_time_series()

    @property
    def series(self) -> pd.Series:
        return self.dataset[self.series_col_name]

    @property
    def times(self) -> pd.Series:
        return self.dataset[self.time_col_name]

    def _load_time_series(self) -> pd.DataFrame:
        if self.file_path.endswith('.csv'):
            return (
                pd.read_csv(self.file_path, parse_dates=[self.time_col_name])
                .assign(**{
                    self.time_col_name: lambda d: pd.to_datetime(
                        d[self.time_col_name], format=self.time_format
                    )
                })
                .sort_values(by=self.time_col_name)
            )
        raise TypeError(
            f"Unexpected file format: {self.file_path.split('.')[-1]}."
        )

    def plot_series(
            self,
            series: Optional[np.ndarray] = None,
            times: Optional[np.ndarray] = None,
            label: Optional[str] = None,
            changepoint: Optional[int] = None
    ) -> None:
        series = series if series is not None else self.series.to_numpy()
        times = times if times is not None else self.times.to_numpy()

        min_len = min(len(series), len(times))
        series, times = series[:min_len], times[:min_len]

        plt.plot(times, series, label=label or "Series")
        if changepoint is not None:
            plt.axvline(times[changepoint], color='red', linestyle='--', label=f'Change @ {changepoint}')
        plt.xlabel("Time")
        plt.ylabel("Series")
        plt.grid(True)
        if label or changepoint is not None:
            plt.legend()
        plt.show()
