"""
Plots: ImagingCI
=================

This example illustrates how to plot an `ImagingCI` dataset using the plotting functions in
`autocti.plot`.
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
__Plotting__

We now pass the first dataset in the imaging to the `aplt.plot_array` function and call it once per
attribute to plot different quantities.
"""
aplt.plot_array(array=dataset_list[0].data, title="Data")
aplt.plot_array(array=dataset_list[0].noise_map, title="Noise Map")
aplt.plot_array(array=dataset_list[0].pre_cti_data, title="Pre CTI Data")

"""
The `aplt.subplot_imaging_ci` function may also plot a subplot of all of these attributes.
"""
aplt.subplot_imaging_ci(dataset=dataset_list[0])

"""
__Regions__

We can also call `aplt.figure_imaging_ci_data_region` which creates 1D plots of regions of the image
binned over the parallel or serial direction.

The regions available are:

 `parallel_fpr`: The charge injection region binned up over all columns (e.g. across serial).
 `parallel_eper`: The parallel CTI trails behind the charge injection region binned up over all columns (e.g.
  across serial).
 `serial_front_edge`: The charge injection region binned up over all rows (e.g. across parallel).
 `serial_trails`: The serial CTI trails behind the charge injection region binned up over all rows (e.g. across serial).
"""
aplt.figure_imaging_ci_data_region(dataset=dataset_list[0], region="parallel_fpr")
aplt.figure_imaging_ci_data_region(dataset=dataset_list[0], region="parallel_eper")

"""
Region plots include the data with error bars showing the noise map.
"""
aplt.figure_imaging_ci_data_region(dataset=dataset_list[0], region="parallel_fpr")
aplt.figure_imaging_ci_data_region(dataset=dataset_list[0], region="parallel_eper")

"""
The above plots can also be created with a logarithmic y axis.
"""
aplt.figure_imaging_ci_data_region(
    dataset=dataset_list[0], region="parallel_fpr", logy=True
)
aplt.figure_imaging_ci_data_region(
    dataset=dataset_list[0], region="parallel_eper", logy=True
)

"""
There is also a subplot of these 1D plots.
"""
aplt.subplot_imaging_ci_region(dataset=dataset_list[0], region="parallel_fpr")

"""
Cosmetic customization of these figures (e.g. drawing the parallel overscan, serial prescan and serial
overscan regions, or a mask and its border) is no longer performed via an `Include2D` object — it is
set via direct keyword arguments to the plotting functions and the `config/visualize.yaml` file.
"""
aplt.plot_array(array=dataset_list[0].data, title="Data")

"""
__Multiple Images__

Our `ImagingCI` dataset consists of many images taken at different charge injection levels. We may wish to plot
all images on the same subplot, which can be performed using the `aplt.subplot_imaging_ci_list` function.
"""
aplt.subplot_imaging_ci_list(dataset_list=dataset_list)

"""
The `aplt.subplot_imaging_ci_data_region_list` function can also plot all of the 1D region figures that we
plotted above, for every dataset on the same subplot.
"""
aplt.subplot_imaging_ci_data_region_list(
    dataset_list=dataset_list, region="parallel_fpr"
)

"""
__Settings Dictionary__

The `settings_dict` of each dataset has entries corresponding to the settings used to create the data. 

For example, this might be the voltages of the charge injections.

This will display on 1D figures when they are plotted, so that when we create a subplot of many datasets we can
see the settings of each dataset.
"""
dataset_list = [
    ac.ImagingCI.from_fits(
        data_path=path.join(dataset_path, f"norm_{int(norm)}", "data.fits"),
        noise_map_path=path.join(dataset_path, f"norm_{int(norm)}", "noise_map.fits"),
        pre_cti_data_path=path.join(
            dataset_path, f"norm_{int(norm)}", "pre_cti_data.fits"
        ),
        layout=layout,
        pixel_scales=0.1,
        settings_dict={"voltage_0": "3V", "voltage_2": "6V"},
    )
    for layout, norm in zip(layout_list, norm_list)
]

aplt.subplot_imaging_ci_data_region_list(
    dataset_list=dataset_list, region="parallel_fpr"
)


"""
Finish.
"""
