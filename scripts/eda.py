import click
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@click.command()
@click.option('--cleaned-data', 'cleaned_data', type=click.Path(exists=True),
              default="data/processed/clean_diabetes.csv", help="Path to read in cleaned data")

@click.option('--plot-output', 'plot_output', type = click.Path(exists=True),
              default = 'results/figures', help='Directory plots will be output to')

@click.option('--table-output', 'table_output', type = click.Path(exists=True),
              default = 'results/tables', help = 'Directory tables will be output to')

def main(cleaned_data, plot_output, table_output):

    diabetes_df = pd.read_csv(cleaned_data)

    with open(os.path.join(table_output, "data_summary.txt"), "w") as f:

        f.write("\n\nData Overview:\n")
   
        diabetes_df.info(buf=f)

    with open(os.path.join(table_output, "descriptive_stats.md"), "w") as f:
        f.write(diabetes_df.describe().to_markdown())



    #target distribution
    sns.histplot(diabetes_df["C_peptide"], kde=True)
    plt.title("Distribution of C_peptide")
    plot_path = os.path.join(plot_output, "c_peptide_distribution.png")
    plt.savefig(plot_path, dpi=300, bbox_inches="tight")
    plt.close()


    #scatterplot matrix
    scatterplot_matrix = sns.pairplot(
        diabetes_df[["Age", "Deficit", "C_peptide"]],
        diag_kind="kde",  
        plot_kws={"alpha": 0.7, "s": 40}  
    )

    plot_path = os.path.join(plot_output, "scatterplot_matrix.png")
    scatterplot_matrix.savefig(plot_path, dpi=300, bbox_inches="tight")
    plt.close()


    #correlation heatmap
    corr = diabetes_df.corr()
    plt.figure(figsize=(6, 4))
    sns.heatmap(corr, annot=True, cmap="coolwarm", center = 0, fmt=".2f")
    plt.title("Correlation Heatmap")

    plot_path = os.path.join(plot_output, "correlation_heatmap.png")
    plt.savefig(plot_path, dpi=300, bbox_inches="tight")
    plt.close()



if __name__ == "__main__":
    main()