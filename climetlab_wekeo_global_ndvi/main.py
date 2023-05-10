#!/usr/bin/env python3
# (C) Copyright 2023 European Centre for Medium-Range Weather Forecasts.
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
from __future__ import annotations

import climetlab as cml
from climetlab import Dataset
from climetlab.decorators import normalize
from climetlab.utils.bbox import BoundingBox

__version__ = "0.1.0"


class Main(Dataset):
    name = "Global 10-daily Normalized Difference Vegetation Index 333M"
    home_page = "https://www.wekeo.eu/data?view=dataset&dataset=EO%3ACLMS%3ADAT%3ACGLS_GLOBAL_NDVI300_V1_333M"
    licence = "https://www.copernicus.eu/en/access-data/copyright-and-licences"
    documentation = "-"
    citation = "-"

    # These are the terms of use of the data (not the licence of the plugin)
    terms_of_use = (
        "By downloading data from this dataset, "
        "you agree to the terms and conditions defined at "
        "https://www.copernicus.eu/en/access-data/copyright-and-licence"
        "If you do not agree with such terms, do not download the data. "
    )

    dataset = None

    default_options = {
        "xarray_open_mfdataset_kwargs": {"chunks": "auto", "engine": "netcdf4"}
    }

    @normalize("start", "date(%Y-%m-%dT%H:%M:%SZ)")
    @normalize("end", "date(%Y-%m-%dT%H:%M:%SZ)")
    def __init__(self, start, end):
        query = {
            "datasetId": "EO:CLMS:DAT:CGLS_GLOBAL_NDVI300_V1_333M",
            "dateRangeSelectValues": [
                {"name": "dtrange", "start": f"{start}", "end": f"{end}"}
            ],
        }
        self.source = cml.load_source("wekeo", query)
        self._xarray = None

    def _to_xarray(self, **kwargs):
        assert len(self) > 0

        options = {}
        options.update(self.default_options)
        options.update(kwargs)

        if len(self) > 1:
            # In this case self.source is a MultiSource instance
            return [s.to_xarray(**options) for s in self.source.sources]

        return self.source._reader.to_xarray(**options)

    def to_bounding_box(self):
        return BoundingBox(north=80, west=-180, south=-60, east=180)

    def bounding_box(self, **kwargs):
        return self.to_bounding_box()

    def to_xarray(self, **kwargs):
        if self._xarray is None:
            self._xarray = self._to_xarray(**kwargs)

        return self._xarray
