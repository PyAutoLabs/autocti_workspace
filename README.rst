PyAutoCTI Workspace
===================

Example scripts and notebooks for simulating, calibrating and correcting charge transfer inefficiency (CTI) in CCD detectors with **PyAutoCTI**. Start with an introduction to CTI, then explore the tools for your own calibration data.

Getting Started
---------------

Explore It Yourself
~~~~~~~~~~~~~~~~~~~

- `Start with the introduction <https://github.com/PyAutoLabs/autocti_workspace/blob/main/notebooks/overview/overview_1_what_is_cti.ipynb>`_ — learn what CTI is and how it affects CCD images.
- `Run it locally <https://pyautocti.readthedocs.io/en/latest/installation/overview.html>`_ — follow the installation guide, then open ``notebooks/overview/overview_1_what_is_cti.ipynb``.
- `Read the documentation <https://pyautocti.readthedocs.io/en/latest/index.html>`_ — explore the concepts and examples in your browser.

See `Find Your Examples`_ below to choose where to start.

Explore with AI
~~~~~~~~~~~~~~~

The `PyAutoCTI AI Assistant <https://github.com/PyAutoLabs/autocti_assistant>`_ helps you learn about CTI and work through calibration examples through conversation. Visit its README for setup instructions and a starting prompt.

Find Your Examples
------------------

Examples are available as Python scripts in ``scripts/`` and Jupyter notebooks in ``notebooks/``.

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - I want to…
     - Start here
   * - Learn about CTI and how calibration works
     - `Overview <https://github.com/PyAutoLabs/autocti_workspace/tree/main/scripts/overview>`_
   * - Simulate or fit one-dimensional CTI data
     - `1D datasets <https://github.com/PyAutoLabs/autocti_workspace/tree/main/scripts/dataset_1d>`_
   * - Simulate or fit charge injection images
     - `Charge injection imaging <https://github.com/PyAutoLabs/autocti_workspace/tree/main/scripts/imaging_ci>`_
   * - Correct data using a CTI model
     - `1D correction <https://github.com/PyAutoLabs/autocti_workspace/tree/main/scripts/dataset_1d/correction>`_ · `Imaging correction <https://github.com/PyAutoLabs/autocti_workspace/tree/main/scripts/imaging_ci/correction>`_
   * - Inspect calibration results
     - `Results <https://github.com/PyAutoLabs/autocti_workspace/tree/main/scripts/dataset_1d/results>`_
   * - Visualise datasets and models
     - `Plotting <https://github.com/PyAutoLabs/autocti_workspace/tree/main/scripts/plot>`_

Each folder has a README explaining its examples. You’ll find sample data in ``dataset/``; analysis results are written to ``output/``.

Learn About CTI
---------------

The `overview examples <https://github.com/PyAutoLabs/autocti_workspace/tree/main/scripts/overview>`_ introduce parallel and serial charge transfer, the features CTI leaves in data, and how to fit and calibrate a CTI model.

For help alongside the examples, ask the PyAutoCTI AI Assistant to explain the detector physics or walk you through a calibration.

Community and Contributing
--------------------------

Ask questions, suggest improvements and share your work in `PyAutoLabs Discussions <https://github.com/orgs/PyAutoLabs/discussions>`_.

To contribute, see the `PyAutoCTI contribution guide <https://github.com/PyAutoLabs/PyAutoCTI/blob/main/CONTRIBUTING.md>`_.

Citations
---------

If you use PyAutoCTI in your research, see the `citation guide <https://github.com/PyAutoLabs/PyAutoCTI/blob/main/CITATIONS.rst>`_.

License
-------

See the `PyAutoCTI license <https://github.com/PyAutoLabs/PyAutoCTI/blob/main/LICENSE>`_.
