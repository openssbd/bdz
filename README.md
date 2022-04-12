# BDZ
**Zarr-based format for storing quantitative biosystems dynamics data**

The following is some progress of storing ROIs and tables for tracking

**These are just test codes to test out ideas**

### Slides for our proposal
https://docs.google.com/presentation/d/1_HGms52mzrZMWRSIeevzlaQ-QS48QBGp-hLFvObKBQo

Some description from the Global BioImaging Hackathon:

Our initial goal was to prepare some kind of container to store the coordinates of biological objects such as the positions of molecules and nuclear contours (and their tracking information) detected by image processing.
However, if, for example, the nuclear contour is represented as a set of vertices, it is difficult to store them in Zarr because of their variable number.
Knowing that there is a framework of AnnData, we think of using OME-Zarr Mask to describe the ROI based on pixels associated with the image, and storing the representative position for biological object in each row of X in AnnData. We think that the features for each biological object such as area, volume, mean value of GFP signal, etc., can be stored in obs.
We think the same issue arises in spatial transcriptome data when describing data for a cell that are detected across multiple pixels.

We think it would be hard to understand without some exmaples, so we would like to create some examples.

We have already developed several data formats based on XML and HDF5, but we want to make a new format highly compatible(?) with OME-NGFF.

### Reference:
- https://doi.org/10.1371/journal.pone.0237468
- https://doi.org/10.1093/bioinformatics/btu767

### Example datasets:

http://so.qbic.riken.jp/ssbd/zarr/v0.3/wt-N2-081015-01.ome.zarr/

Kyoda, K., Okada, H., Itoga, H. and Onami, S.: ‘Deep Collection of Quantitative Nuclear Division Dynamics Data in RNAi-Treated Caenorhabditis Elegans Embryos’. bioRxiv, https://doi.org/10.1101/2020.10.04.325761.

### Sample viewing with napari image viewer

It requires the module from Kevin Yamauchi:
https://github.com/kevinyamauchi/ome-ngff-tables-prototype
```
pip install git+https://github.com/kevinyamauchi/ome-ngff-tables-prototype
```

![screenshot01](https://user-images.githubusercontent.com/17229969/162355694-a37fa183-3407-4e37-a855-5cbac19c85b7.png)
![screenshot02](https://user-images.githubusercontent.com/17229969/162355708-9380052a-3f8d-470e-ba5c-1113f4710b48.png)
