"""
Plots: Dataset1D
================

This example illustrates how to plot a `Dataset1D` dataset using the plotting functions in
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
__dataset__

Load the dataset 'dataset_1d/simple' from .fits files, which is the dataset we will use to illustrate plotting
the dataset.
"""
dataset_name = "simple"
dataset_path = path.join("dataset", "dataset_1d", dataset_name)

shape_native = (200, 1)

prescan = ac.Region1D((0, 10))
overscan = ac.Region1D((190, 200))

region_list = [(10, 20)]

norm_list = [100, 5000, 25000, 200000]

layout_list = [
    ac.Layout1D(
        shape_1d=shape_native,
        region_list=region_list,
        prescan=prescan,
        overscan=overscan,
    )
    for norm in norm_list
]

dataset_list = [
    ac.Dataset1D.from_fits(
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

We now pass the first dataset to the plotting functions, which plot its different attributes.

The `figure_dataset_1d_data` function plots the data as a 1D errorbar figure (with the noise map
as error bars); `logy=True` uses a logarithmic y axis. The `output_path` / `output_format` inputs
save the figure to hard-disk.
"""
output_path = path.join(".")

aplt.figure_dataset_1d_data(
    dataset=dataset_list[0], logy=True, output_path=output_path, output_format="png"
)

"""
The `subplot_dataset_1d` function plots a subplot of the data, noise map, signal-to-noise map and
pre-CTI data.
"""
aplt.subplot_dataset_1d(
    dataset=dataset_list[0], output_path=output_path, output_format="png"
)

"""
__Regions__

Specific regions of the data can be extracted and plotted, for example the EPER or FPR.

Region plots include the data with error bars showing the noise map.
"""
aplt.figure_dataset_1d_data(dataset=dataset_list[0], region="fpr")
aplt.figure_dataset_1d_data(dataset=dataset_list[0], region="eper")

"""
The above plots can also be created with a logarithmic y axis.
"""
aplt.figure_dataset_1d_data(dataset=dataset_list[0], region="fpr", logy=True)
aplt.figure_dataset_1d_data(dataset=dataset_list[0], region="eper", logy=True)

"""
__Multiple Images__

Our `Dataset1D` dataset consists of many images taken at different charge injection levels. We may
wish to plot all images on the same subplot, which is performed using the `subplot_dataset_1d_list`
function.
"""
aplt.subplot_dataset_1d_list(dataset_list=dataset_list)

"""
__Settings Dictionary__

The `settings_dict` of each dataset has entries corresponding to the settings used to create the data.

For example, this might be the voltages of the charge injections.

This will display on 1D figures when they are plotted, so that when we create a subplot of many datasets we can
see the settings of each dataset.
"""
dataset_list = [
    ac.Dataset1D.from_fits(
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

aplt.subplot_dataset_1d_list(dataset_list=dataset_list)

"""
Finish.
"""
