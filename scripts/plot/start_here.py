"""
Plots: Start Here
=================

This example introduces the plotting API in PyAutoCTI.

The old API (removed) used `*Plotter` classes (e.g. `Dataset1DPlotter`, `ImagingCIPlotter`) together
with `MatPlot1D` / `MatPlot2D` and `Visuals1D` / `Visuals2D` helper objects. These have all been
removed.

The new API uses standalone functions:

 - `aplt.plot_array()` — plot any 2D array (e.g. charge injection data).
 - `aplt.plot_cti_1d()` — plot any 1D quantity with CTI conventions (errorbars, log-y, zero line).
 - `aplt.subplot_dataset_1d()`, `aplt.subplot_imaging_ci()`, `aplt.subplot_fit_ci()`, etc. —
   multi-panel subplots for standard objects.

__Contents__

- **Dataset:** Load and plot a 1D CTI calibration dataset.
- **Regions:** Extract and bin the FPR / EPER regions of the data in 1D figures.
- **Customization:** Each plotting function accepts direct keyword arguments.
- **Config Defaults:** Default plotting values come from the `config/visualize.yaml` file.
- **Charge Injection:** 2D plots and binned region plots of `ImagingCI` data.
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

First, lets load an example `Dataset1D`, which we will use to illustrate the 1D plotting API.

You should be familiar with how we load datasets in this way, if not checkout the `overview`
and `modeling/start_here.py` examples.
"""
dataset_name = "simple"
dataset_path = path.join("dataset", "dataset_1d", dataset_name)
shape_native = (200,)

prescan = ac.Region1D(region=(0, 10))
overscan = ac.Region1D(region=(190, 200))

region_list = [(10, 20)]

norm_list = [100]

total_datasets = len(norm_list)

layout_list = [
    ac.Layout1D(
        shape_1d=shape_native,
        region_list=region_list,
        prescan=prescan,
        overscan=overscan,
    )
    for i in range(total_datasets)
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

dataset = dataset_list[0]

"""
__Individual Figures__

The `aplt.figure_dataset_1d_data()` function plots the data of a `Dataset1D` as a 1D errorbar
figure, with the noise map as error bars.
"""
aplt.figure_dataset_1d_data(dataset=dataset)

"""
__Subplots__

The `aplt.subplot_dataset_1d()` function produces a multi-panel overview of the dataset: the data,
noise map, signal-to-noise map and pre-CTI data.
"""
aplt.subplot_dataset_1d(dataset=dataset)

"""
__Regions__

CTI calibration interprets specific regions of the data — the FPR (first pixel response, the
injected signal) and the EPER (extended pixel edge response, the CTI trail). Passing a `region`
string extracts and bins the data over that region.

EPER trails span orders of magnitude, so a log10 y-axis (`logy=True`) is often clearer.
"""
aplt.figure_dataset_1d_data(dataset=dataset, region="fpr")
aplt.figure_dataset_1d_data(dataset=dataset, region="eper", logy=True)

aplt.subplot_dataset_1d(dataset=dataset, region="eper")

"""
__Customization__

Each plotting function accepts direct keyword arguments for customization:

 - `title_prefix`: A string prefixed to every panel title.
 - `output_path`: Directory path to save the figure on disk.
 - `output_format`: Format of the saved file, e.g. "png" or "pdf".

These replace the old `MatPlot1D` / `MatPlot2D` objects entirely — there is no `MatPlot` anymore.
Figure-level cosmetics (fontsizes, figure sizes) are set via the config files (see below).
"""
aplt.figure_dataset_1d_data(
    dataset=dataset,
    output_path=path.join("output", "plot"),
    output_format="png",
)

"""
__Config Defaults__

Default plotting values (figure sizes, fontsizes, output behaviour during model fits) are
configured via:

  autocti_workspace/config/visualize.yaml

When no explicit keyword is passed to a plotting function the config value is used, allowing the
default appearance to be controlled workspace-wide without changing code.

__Multiple Datasets__

CTI calibration datasets typically span many injection normalizations. The `*_list` functions plot
one panel per dataset.
"""
aplt.subplot_dataset_1d_list(dataset_list=dataset_list, region="eper", logy=True)

"""
__Charge Injection Data__

2D charge injection data (`ImagingCI`) has its own subplot and region functions. The 2D primitives
are `aplt.plot_array()` for any `Array2D` and `aplt.subplot_imaging_ci()` for the dataset overview:

 - `aplt.subplot_imaging_ci(dataset=dataset)` — data, noise map, S/N, pre-CTI data (+ cosmic rays).
 - `aplt.figure_imaging_ci_data_region(dataset=dataset, region="parallel_eper")` — binned 1D
   region figures ("parallel_fpr", "parallel_eper", "serial_fpr", "serial_eper").
 - `aplt.subplot_imaging_ci_data_binned(dataset=dataset)` — the data binned over rows / columns
   with and without the FPR, revealing injection non-uniformity and calibration systematics.

The `imaging_ci` example scripts illustrate these on simulated charge injection data.

__Fits__

Fits to CTI datasets have matching functions: `aplt.subplot_fit_dataset_1d()`,
`aplt.figure_fit_dataset_1d()` (any fit quantity, e.g. `quantity="residual_map"`),
`aplt.subplot_fit_ci()` and `aplt.figure_fit_ci_region()` — see the `plot/plotters` examples.

__Searches__

Model-fits using a non-linear search produce search-specific visualization via
`aplt.corner_anesthetic()`, `aplt.corner_cornerpy()` and related functions.

Finish.
"""
