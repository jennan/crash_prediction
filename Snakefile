rule all:
    input:
        "results/cas_dataset.csv",
        "results/linear_model/predictions.csv",
        "results/mlp_model/predictions.csv"

rule download_data:
    output:
        "data/cas_dataset.csv"
    shell:
        "cas_data download {output}"

rule prepare_data:
    input:
        "data/cas_dataset.csv"
    output:
        "results/cas_dataset.csv"
    shell:
        "cas_data prepare {input} -o {output}"

rule fit_model:
    input:
        "results/cas_dataset.csv"
    output:
        "results/{model_name}_model/model.pickle"
    shell:
        "sklearn_models fit-{wildcards.model_name} {input} -o {output} -v"

rule predict:
    input:
        "results/cas_dataset.csv",
        "results/{model_name}_model/model.pickle"
    output:
        "results/{model_name}_model/predictions.csv"
    shell:
        "sklearn_models predict {input} -o {output}"