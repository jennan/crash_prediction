# # Exploration of the crash severity information in CAS data
#
# In this notebook, we will explore the severity of crashes, as it will be the
# target of our predictive models.

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

from crash_prediction import cas_data

# set seaborn default style
sb.set()

# But first, we ensure we have the data or download it if needed

dset_path = Path("..") / "data" / "cas_dataset.csv"
if not dset_path.exists():
    cas_data.download(dset_path)

# and load it.

dset = pd.read_csv(dset_path)
dset.head()

# The CAS dataset has 4 features that can be associated with the crash severity:
#
# - `crashSeverity`, severity of a crash, determined by the worst injury
#    sustained in the crash at time of entry,
# - `fatalCount`, count of the number of fatal casualties associated with this
#   crash,
# - `minorInjuryCount`, count of the number of minor injuries associated with
#   this crash,
# - `seriousInjuryCount`, count of the number of serious injuries associated
#   with this crash.

severity_features = [
    "fatalCount",
    "seriousInjuryCount",
    "minorInjuryCount",
    "crashSeverity",
]

fig, axes = plt.subplots(2, 2, figsize=(15, 12))
for ax, feat in zip(axes.flat, severity_features):
    counts = dset[feat].value_counts(dropna=False)
    counts.plot.bar(ylabel="# crashes", title=feat, ax=ax)
    ax.set(yscale="log")
fig.tight_layout()

# To check the geographical distribution, we will focus on Auckland and replace
# discrete levels of `crashSeverity` with number to ease plotting.

dset_auckland = dset[dset["X"].between(174.7, 174.9) & dset["Y"].between(-37, -36.8)]

mapping = {
    "Non-Injury Crash": 1,
    "Minor Crash": 2,
    "Serious Crash": 3,
    "Fatal Crash": 4,
}
dset_auckland = dset_auckland.replace({"crashSeverity": mapping})

# Given the data set imbalance, we plot the local maxima to better see the
# location of more severe car crashes.

fig, axes = plt.subplots(2, 2, figsize=(15, 15))
for ax, feat in zip(axes.flat, severity_features):
    dset_auckland.plot.hexbin(
        "X",
        "Y",
        feat,
        gridsize=500,
        reduce_C_function=np.max,
        cmap="BuPu",
        title=feat,
        ax=ax,
        sharex=False,
    )
    ax.set_xticklabels([])
    ax.set_yticklabels([])
fig.tight_layout()

# Few remarks coming from these plots:
#
# - fatal counts are (hopefully) very low,
# - crashes with serious injuries are also very sparse,
# - crashes with minor injuries are denser and seem to follow major axes,
# - the crash severity feature looks like the most homogeneous feature, yet
#   highlighting some roads more than others.
#
# The crash severity is probably a good go-to target, as it's quite
# interpretable and actionable. The corresponding ML problem is a supervised
# multi-class prediction problem.

# ---
# ## Original computing environment

# !date -R

# !uname -a

# !pip freeze