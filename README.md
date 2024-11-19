# ViNo
**Vi**deo An**no**tation Tool



## Environment
Better to create virtual env to avoid environment variable issues on Windows.
```
# creat and activate conda virtual environment
conda create -n ViNo python=3.9.19
conda activate ViNo

# get repo and to the latest-dev branch
git clone 
git fetch --all
git checkout latest-dev

# install as editable way
pip install -e .
```

## Basic Usage
* Use ``vino-start`` to start the annotation tool. 
* Setup csv index in ``projects/coche/index_csv`` folder.
* Annotation will be generated in ``projects/coche/annotation``.
* Use ``A`` and ``D`` to move backward/forward continuously for a video.
* Use ``Q`` and ``E`` to move backward/forward single-frame-wise for a video.
* Use ``Cmd/Ctrl+S`` to save the annotation.