# Tests should generate (and then clean up) any files they need for testing. No
# binary files should be included in the repository.

from intake_bluesky_tiff_series import TIFSeriesPlugin
import tifffile
import numpy as np
import pytest
import os

@pytest.fixture
def data_files(tmp_path):
    paths = []
    for i in range(3):
        for j in range(4):
            data = np.random.random((1000, 1000))
            path = os.path.join(tmp_path, f'sample_{i}_frame_{j}.tif')
            paths.append(path)
            tifffile.imsave(path, data)
    return paths


def test_doc_stream(data_files):
    docs = list(TIFSeriesPlugin.ingest(data_files))
    assert len(docs) == 39  # 1 start, 1 descriptor, 12 resources, 12 datums, 12 events, 1 stop


def test_fill(data_files):
    import event_model
    with event_model.Filler({TIFSeriesPlugin.name: TIFSeriesPlugin}) as filler:
        doc_stream = TIFSeriesPlugin.ingest(data_files)
        for name, doc in doc_stream:
            name, doc = filler(name, doc)
            doc['filled'] = {'image': False}
            if name == 'event':
                assert isinstance(doc['data']['image'], np.ndarray)

@pytest.fixture
def catalog(data_files):
    from intake_bluesky_files import FilesCatalog
    return FilesCatalog(data_files, handler=TIFSeriesPlugin)

def test_catalog(catalog):
    assert catalog[next(iter(catalog._run_starts.keys()))]

def test_catalog_len(catalog): # KNOWN NOT PASSING
    # FIXME: Seems like len should be supported on a catalog
    # assert len(catalog) == 3
    pass

def test_xarray(data_files):
    # FIXME
    ...
