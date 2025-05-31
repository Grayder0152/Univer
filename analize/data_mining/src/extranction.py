import os
from typing import Optional

import polars as pl

from settings import SAMPLE_DATASETS_DIR


def detect_delimiter(csv_file: str) -> str:
    possible_delimiters = [";", ",", " ", "|"]
    with open(os.path.join(SAMPLE_DATASETS_DIR, csv_file), 'r') as f:
        header = f.readline()

        for delimiter in possible_delimiters:
            if header.find(delimiter) != -1:
                return delimiter
    return ","


def extract(file_name: str, columns: Optional[list[str]] = None, delimiter: Optional[str] = None) -> pl.DataFrame:
    if delimiter is None:
        delimiter = detect_delimiter(file_name)

    df = pl.read_csv(os.path.join(SAMPLE_DATASETS_DIR, file_name), separator=delimiter)
    if columns is not None:
        df = df[columns]
    return df
