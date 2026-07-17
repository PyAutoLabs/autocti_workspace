"""
Plots: MultiFigurePlotter
=========================

This example illustrates how to plot the same figure from multiple datasets on the same subplot.

An example of when to use this would be when two different datasets (e.g. two charge injection datasets) are
loaded and visualized, and the images of each dataset are plotted on the same subplot side-by-side. This is the example
we will use in this example script.

This uses the `*_list` family of plotting functions (e.g. `aplt.subplot_imaging_ci_list`), which require only a
list of datasets to be passed to them. Each `*_list` function plots the same figure from every dataset in the list
on the same subplot.
"""

# %matplotlib inline
# from pyprojroot import here
# workspace_path = str(here())
# %cd $workspace_path
# print(f"Working Directory has been set to `{workspace_path}`")

from os import path
import autocti as ac
import autocti.plot as aplt

"""
__Dataset__

Load the charge injection dataset 'imaging_ci/uniform/parallel_x2' from .fits files, which is the dataset we will
use to illustrate plotting charge injection data.
"""

shape_native = (2000, 100)

dataset_name = "simple"
dataset_path = path.join("dataset", "imaging_ci", dataset_name)

parallel_overscan = ac.Region2D((1980, 2000, 5, 95))
serial_prescan = ac.Region2D((0, 2000, 0, 5))
serial_overscan = ac.Region2D((0, 1980, 95, 100))

regions_list = [
    (0, 200, serial_prescan[3], serial_overscan[2]),
    (400, 600, serial_prescan[3], serial_overscan[2]),
    (800, 1000, serial_prescan[3], serial_overscan[2]),
    (1200, 1400, serial_prescan[3], serial_overscan[2]),
    (1600, 1800, serial_prescan[3], serial_overscan[2]),
]

norm_list = [100, 5000, 25000, 200000]

total_datasets = len(norm_list)

layout_list = [
    ac.Layout2DCI(
        shape_2d=shape_native,
        region_list=regions_list,
        parallel_overscan=parallel_overscan,
        serial_prescan=serial_prescan,
        serial_overscan=serial_overscan,
    )
    for i in range(total_datasets)
]

dataset_list = [
    ac.ImagingCI.from_fits(
        data_path=path.join(dataset_path, f"norm_{int(norm)}", "data.fits"),
        noise_map_path=path.join(dataset_path, f"norm_{int(norm)}", "noise_map.fits"),
        pre_cti_data_path=path.join(
            dataset_path, f"norm_{int(norm)}", "pre_cti_data.fits"
        ),
        layout=layout,
        pixel_scales=0.1,
    )
    for layout, norm in zip(layout_list, norm_list)
]


"""
__Plot__

Plot the subplot of each `ImagingCI` dataset individually using the `aplt.subplot_imaging_ci` function.
"""
for dataset in dataset_list:
    aplt.subplot_imaging_ci(dataset=dataset)

"""
__Multi Plot__

We now pass the list of datasets to the `aplt.subplot_imaging_ci_list` function, which plots the same figure
(the data) from each dataset on the same subplot.
"""
aplt.subplot_imaging_ci_list(dataset_list=dataset_list)

"""
__Wrap Up__

In the simple example above, we used `aplt.subplot_imaging_ci_list` to plot the same figure (the data) from each
`ImagingCI` dataset on the same `matplotlib` subplot.

Every dataset and fit object in `autocti.plot` has a matching `*_list` function (e.g.
`aplt.subplot_dataset_1d_list`, `aplt.subplot_fit_ci_list`, `aplt.subplot_fit_dataset_1d_list`), each of which
plots the same figure from a list of objects on the same subplot.
"""
