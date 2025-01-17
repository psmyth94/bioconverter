from typing import Any, Dict

import numpy as np
import pandas as pd
import pyarrow as pa

from biocore.utils.import_util import requires_backends
from biocore.utils.inspect import (
    get_kwargs,
    np_array_kwargs,
    np_asarray_kwargs,
    pa_table_from_pandas_kwargs,
)

from ..dict import DictConverter


class RowDictConverter(DictConverter):
    dtype = "Dict[str, Any]"

    def to_list(self, X: Dict[str, Any], **kwargs):
        return [X]

    def to_dict(self, X: Dict[str, Any], **kwargs):
        return X

    def to_dicts(self, X: Dict[str, Any], **kwargs):
        return [X]

    def to_numpy(self, X: Dict[str, Any], **kwargs):
        if np.lib.NumpyVersion(np.__version__) >= "2.0.0b1":
            return np.asarray(self.to_list(X, **kwargs), **np_asarray_kwargs(kwargs))
        return np.array(self.to_list(X, **kwargs), **np_array_kwargs(kwargs))

    def to_pandas(self, X: Dict[str, Any], **kwargs):
        return pd.DataFrame([X], **get_kwargs(kwargs, pd.DataFrame.__init__))

    def to_series(self, X: Dict[str, Any], **kwargs):
        return pd.Series(X, **get_kwargs(kwargs, pd.Series.__init__))

    def to_polars(self, X: Dict[str, Any], **kwargs):
        requires_backends(self.to_polars, "polars")
        import polars as pl

        return pl.DataFrame([X], **get_kwargs(kwargs, pl.DataFrame.__init__))

    def to_arrow(self, X: Dict[str, Any], **kwargs):
        return pa.Table.from_pandas(
            self.to_pandas(X, **kwargs), **pa_table_from_pandas_kwargs(kwargs)
        )

    def to_dataset(self, X: Dict[str, Any], **kwargs):
        requires_backends(self.to_dataset, "datasets")
        from datasets import Dataset

        return Dataset.from_pandas(
            self.to_pandas(X, **kwargs), **get_kwargs(kwargs, Dataset.from_pandas)
        )

    def to_bioset(self, X: Dict[str, Any], **kwargs):
        requires_backends(self.to_bioset, "biosets")
        from biosets import Bioset

        return Bioset.from_pandas(
            self.to_pandas(X, **kwargs), **get_kwargs(kwargs, Bioset.from_pandas)
        )

    def to_iterabledataset(self, X: Dict[str, Any], **kwargs):
        requires_backends(self.to_iterabledataset, "datasets")
        from datasets import IterableDataset

        def gen(**gen_kwargs):
            yield X

        return IterableDataset.from_generator(
            gen, **get_kwargs(kwargs, IterableDataset.from_generator)
        )

    def to_dask(self, X: Dict[str, Any], **kwargs):
        requires_backends(self.to_dask, "dask")
        import dask.dataframe as dd

        return dd.from_pandas(
            self.to_pandas(X, **kwargs), **get_kwargs(kwargs, dd.from_pandas)
        )

    def to_ray(self, X, **kwargs):
        requires_backends(self.to_ray, "ray")
        import ray.data

        return ray.data.from_items(X, **get_kwargs(kwargs, ray.data.from_items))
