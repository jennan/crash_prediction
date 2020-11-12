import typing as T
from pathlib import Path

import defopt
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

import sklearn.metrics as metrics
from sklearn.calibration import calibration_curve


def plot_calibration_curves(dset, ax=None):
    if ax is None:
        _, ax = plt.subplots()

    ax.plot([0, 1], [0, 1], "--k")

    for key, group in dset.groupby("fold"):
        prob_true, prob_pred = calibration_curve(group["injuryCrash"], group["y_prob"])
        ax.plot(prob_true, prob_pred, "-o", label=key)

    ax.grid(True)
    ax.set_xlabel("True probabilities")
    ax.set_ylabel("Predicted probabilities")
    ax.legend()

    return ax


def plot_roc_curves(dset, ax=None):
    if ax is None:
        _, ax = plt.subplots()

    ax.plot([0, 1], [0, 1], "k--")

    for key, group in dset.groupby("fold"):
        fpr, tpr, _ = metrics.roc_curve(group["injuryCrash"], group["y_prob"])
        ax.plot(fpr, tpr, label=key)

    ax.grid(True)
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate")
    ax.legend()

    return ax


def plot_precision_recall(dset, ax=None):
    if ax is None:
        _, ax = plt.subplots()

    for key, group in dset.groupby("fold"):
        precision, recall, _ = metrics.precision_recall_curve(
            group["injuryCrash"], group["y_prob"]
        )
        ax.plot(recall, precision, label=key)

    ax.grid(True)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.legend()

    return ax


METRICS_FCN = {
    "accuracy": metrics.accuracy_score,
    "F1": metrics.f1_score,
    "precision": metrics.precision_score,
    "recall": metrics.recall_score,
}


def score(dset_file: Path, preds_file: Path, output_folder: Path):
    """Score and plots results

    :param dset_file: CAS dataset .csv file
    :param pred_file: predictions .csv file
    :param output_folder: output folder for the figures
    """
    dset = pd.read_csv(dset_file, usecols=["injuryCrash", "fold"])
    dset["y_prob"] = pd.read_csv(preds_file)
    dset["y_pred"] = dset["y_prob"] > 0.5

    output_folder.mkdir(parents=True, exist_ok=True)

    # generate scores for each defined metric
    def score_fold(x):
        scores = {
            key: metric_fcn(x["injuryCrash"], x["y_pred"])
            for key, metric_fcn in METRICS_FCN.items()
        }
        scores["neg_log_loss"] = metrics.log_loss(x["injuryCrash"], x["y_prob"])
        scores["roc_auc"] = metrics.roc_auc_score(x["injuryCrash"], x["y_prob"])
        return pd.Series(scores)

    scores = dset.groupby("fold").apply(score_fold).reset_index()
    scores.to_csv(output_folder / "scores.csv", index=False)

    # plot calibration, ROC and precision/recall curves
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    plot_roc_curves(dset, ax=axes[0])
    axes[0].set_title("ROC curve")

    plot_precision_recall(dset, ax=axes[1])
    axes[1].set_title("Precision-Recall curve")

    plot_calibration_curves(dset, ax=axes[2])
    axes[2].set_title("Calibration curve")

    fig.tight_layout()
    fig.savefig(output_folder / "curves.png")


def summarize(output_folder: Path, *score_file: Path, labels: T.Iterable[str] = ()):
    """Generate summary plot and table

    :param output_folder: directory to save figures (plots and tables)
    :param score_file: CSV file containing scores for one method
    :param labels: method name for each input dataset file
    """

    # use input filenames as labels if none are given
    if not labels:
        labels = [str(fname) for fname in score_file]

    # merge together all scores dataframes
    scores = [pd.read_csv(fname) for fname in score_file]
    scores = [pd.melt(score, id_vars="fold", var_name="metric") for score in scores]
    scores = pd.concat([df.assign(label=label) for df, label in zip(scores, labels)])

    # save the combined dataframe
    output_folder.mkdir(parents=True, exist_ok=True)
    scores.to_csv(output_folder / "summary.csv", index=False)

    # plot scores in a grid and save the figure
    scores = scores.sort_values(["label"])
    grid = sb.FacetGrid(data=scores, col="metric", sharey=False, col_wrap=3)
    grid.map_dataframe(
        sb.barplot, x="label", y="value", hue="fold", hue_order=["train", "test"]
    )
    grid.set_xticklabels(rotation=45, ha="right")
    grid.add_legend()
    grid.fig.savefig(output_folder / "summary.png", bbox_inches="tight")


def main():
    defopt.run([score, summarize])
