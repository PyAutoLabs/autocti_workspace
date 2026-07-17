"""
Plots: Well Filling
===================

The well filling behaviour of a CCD is fitted for in a CTI model fit.

However, a visual showing the behaviour before the fit can be produced.
"""

# %matplotlib inline
# from pyprojroot import here
# workspace_path = str(here())
# %cd $workspace_path
# print(f"Working Directory has been set to `{workspace_path}`")

import os

import matplotlib.pyplot as plt
import numpy as np
from os import path
import autocti as ac
import autocti.plot as aplt

"""
__Dataset__

Load the CTI dataset 'imaging_ci/simple' 'from .fits files, which is the dataset we will use to perform CTI modeling.
"""
dataset_name = "simple"
dataset_path = path.join("dataset", "imaging_ci", dataset_name)

shape_native = (2000, 100)

parallel_overscan = ac.Region2D((1980, 2000, 5, 95))
serial_prescan = ac.Region2D((0, 2000, 0, 5))
serial_overscan = ac.Region2D((0, 1980, 95, 100))

region_list = [
    (0, 200, serial_prescan[3], serial_overscan[2]),
    (400, 600, serial_prescan[3], serial_overscan[2]),
    (800, 1000, serial_prescan[3], serial_overscan[2]),
    (1200, 1400, serial_prescan[3], serial_overscan[2]),
    (1600, 1800, serial_prescan[3], serial_overscan[2]),
]


norm_list = [100, 5000, 25000, 200000]

workspace_path = os.getcwd()

total_datasets = len(norm_list)

layout_list = [
    ac.Layout2DCI(
        shape_2d=shape_native,
        region_list=region_list,
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

injection_norm_list = [
    np.mean(
        layout.extract.parallel_fpr.median_list_from(
            array=dataset.data, settings=ac.SettingsExtract(pixels=(50, 200))
        ),
    )
    for dataset, layout in zip(dataset_list, layout_list)
]


eper_list = [
    float(
        layout.extract.parallel_eper.binned_array_1d_from(
            array=dataset.data,
            settings=ac.SettingsExtract(pixels=(0, 1)),
        )
    )
    for dataset, layout in zip(dataset_list, layout_list)
]

print(eper_list)

beta_0 = np.asarray(injection_norm_list) ** (0.5)
beta_1 = 0.5 * np.asarray(injection_norm_list) ** (0.5)
beta_2 = 0.1 * np.asarray(injection_norm_list) ** (0.5)

# f = 1
#
# beta_0 = np.asarray(injection_norm_list)**(0.3)
# beta_1 = np.asarray(injection_norm_list)**(0.5)
# beta_2 = np.asarray(injection_norm_list)**(0.7)

"""
__Plot__

The `aplt.plot_yx()` function plots the EPER signal against the injection level. `xtick_suffix` /
`ytick_suffix` append the electron unit ("e-") to the tick labels, replicating the old `Units` /
`XTicks` / `YTicks` customization.
"""
fig, ax = plt.subplots(figsize=(10, 10))

aplt.plot_yx(
    y=eper_list,
    x=injection_norm_list,
    ax=ax,
    plot_axis_type="scatter",
    xlabel="Injection Level",
    ylabel="Electrons in First Parallel EPER Pixel",
    xtick_suffix="e-",
    ytick_suffix="e-",
)

fig.savefig(path.join(workspace_path, "well_filling.png"))
plt.close(fig)

"""
The well filling behaviour is also plotted on a log-log axis, alongside three reference power-law
curves (`beta_0`, `beta_1`, `beta_2`) for comparison against the data.
"""
fig, ax = plt.subplots(figsize=(10, 10))

aplt.plot_yx(
    y=eper_list,
    x=injection_norm_list,
    ax=ax,
    plot_axis_type="loglog",
    y_extra=beta_0,
    xlabel="Injection Level",
    ylabel="Electrons in First Parallel EPER Pixel",
    xtick_suffix="e-",
    ytick_suffix="e-",
)
ax.plot(injection_norm_list, beta_1, color="g", linestyle="--", alpha=0.7)
ax.plot(injection_norm_list, beta_2, color="b", linestyle="--", alpha=0.7)

fig.savefig(path.join(workspace_path, "well_filling_loglog.png"))
plt.close(fig)
