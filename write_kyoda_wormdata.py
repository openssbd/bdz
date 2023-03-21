import pandas as pd
import os
import glob
import anndata as ad
from scipy.sparse import csr_matrix
import numpy as np
from ome_zarr.io import parse_url
import zarr
from ngff_tables_prototype.writer import write_table_points


df = pd.read_csv('wt-N2-081015-01.csv', names=('t', 'pid', 'cid', 'x', 'y', 'z', 'name', 'sphericity', 'volume', 'phase'))
df['entity'] = 'line'


print(df.head())

print(df)


n_obs, n_vars = 65, 4
nmp = df[["t", "z", "y", "x"]].values
Y = nmp
X1 = Y / np.array([1, 0.5016, 0.1015, 0.1015])
X2 = X1 * np.array([1, -1, 1, 1])
X = X2 + np.array([0, 65, 0, 0])

dfa = pd.DataFrame(X, columns=list('tzyx'), index=np.arange(n_obs, dtype=int).astype(str))

# print("X", X)

# print("dfa", dfa)
# t          z           y           x
# 0    1.0  39.922648  109.316256  307.414778
# 1    2.0  39.498206  113.885714  309.511330
# 2    3.0  39.999203  111.549754  315.685714

obs_raw = df.loc[:,["cid", "entity", "name", "sphericity", "volume"]]

obs_meta = obs_raw.rename(columns={'cid': 'id'})

col = obs_meta.loc[:, 'id']
col.transpose()

# NB: use int8 to allow viewing in web
obsp_raw = np.loadtxt('wt-N2-081015-01-track.csv', delimiter=',', dtype=np.int8)
obsp_meta = pd.DataFrame(obsp_raw, index = col.astype(str), columns = col.astype(str))

# print(obsp_meta)
# id     1000  2000  3000  4000  5000  6000  7000  8000  9000  10000  ...  46000  46001  47000  47001  48000  48001  49000  49001  50000  50001
# id                                                                  ...                                                                      
# 1000      0     1     0     0     0     0     0     0     0      0  ...      0      0      0      0      0      0      0      0      0      0
# 2000      0     0     1     0     0     0     0     0     0      0  ...      0      0      0      0      0      0      0      0      0      0
# 3000      0     0     0     1     0     0     0     0     0      0  ...      0      0      0      0      0      0      0      0      0      0


adata = ad.AnnData(X = dfa, obs = obs_meta)

# write as sparse data to obsp
adata.obsp["tracking"] = csr_matrix(obsp_raw)

store = parse_url("wt-N2-081015-01.ome.zarr", mode="w").store
root = zarr.group(store=store)

tables_group = root.create_group(name="tables")
write_table_points(
    group=tables_group,
    adata=adata
)
