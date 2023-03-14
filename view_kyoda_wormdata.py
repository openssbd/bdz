import os
import zarr
import numpy as np
from anndata import AnnData
from anndata._io import read_zarr
from ome_zarr.io import parse_url
from ome_zarr.reader import Reader
import napari
from napari_ome_zarr._reader import transform
from napari.types import LayerDataTuple

from ngff_tables_prototype.reader import load_table_to_anndata, get_napari_points_layer_data


def check_div(tracks_matrix, n):
    next = 0
    for i in range(len(tracks_matrix[n])):
            if tracks_matrix[n][i] == 1:
                next += 1
    return next

def track_obj(tracks_matrix, m, points_coords, tracks, tid):
    if check_div(tracks_matrix, m) == 1:
        tracks = np.append(tracks, np.insert(points_coords[m], 0, tid))
        for i in range(len(tracks_matrix[m])):
            if tracks_matrix[m][i] == 1:
                tracks_matrix[m][i] = 2
                tracks = track_obj(tracks_matrix, i, points_coords, tracks, tid)
        return tracks
    else:
        return tracks
                
def _anndata_to_napari_tracks(anndata_obj: AnnData) -> LayerDataTuple:
    points_coords = anndata_obj.X
    tracks_matrix = anndata_obj.obsm["tracking"]
    tracks = np.empty((0, 5))
    
    tid = 0
    for i in range(len(tracks_matrix)):
        for j in range(len(tracks_matrix[i])):
            if tracks_matrix[i][j] == 1:
                tracks = np.append(tracks, np.insert(points_coords[i], 0, tid))
                tracks = track_obj(tracks_matrix, j, points_coords, tracks, tid)
                tid += 1

    t = tracks.reshape([tracks.size // 5, 5])

    return t, "", 'tracks'


def load_to_napari_layer_bdz(file_path: str):
    ome_zarr = parse_url(file_path)
    reader = Reader(ome_zarr)
    reader_func = transform(reader())
    layer_data = reader_func(file_path)

    TABLES_DIR = "tables"
    table_group = zarr.group(store=ome_zarr.store, path=TABLES_DIR)
    table_attrs = table_group.attrs.asdict()
    print("table_attrs", table_attrs)

    # assume just one table...
    table_name = table_attrs["tables"][0]
    table_path = os.path.join(TABLES_DIR, table_name)
    print("loading points data from ", table_path)

    # load points points
    points_layer = get_napari_points_layer_data(file_path, table_path)
    layer_data.append(points_layer)

    # load tracking info. (added)
    anndata_obj = load_table_to_anndata(file_path, table_path)
    layer_data.append(_anndata_to_napari_tracks(anndata_obj))
    
    return layer_data

def load_to_napari_viewer_bdz(file_path: str) -> napari.Viewer:
    layer_data = load_to_napari_layer_bdz(file_path)

    viewer = napari.Viewer()

    for layer in layer_data:
        viewer._add_layer_from_data(*layer)
    return viewer

viewer = load_to_napari_viewer_bdz(file_path='wt-N2-081015-01.ome.zarr')
napari.run()

