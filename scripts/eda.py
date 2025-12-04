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

def main(cleaned_data, plot_output):

    diabetes_df = pd.read_csv(cleaned_data)

    print(diabetes_df.info())

    print(diabetes_df.describe())

    sns.histplot(diabetes_df["C_peptide"], kde=True)
    plt.title("Distribution of C_peptide")
    plot_path = os.path.join(plot_output, "c_peptide_distribution.png")
    plt.savefig(plot_path, dpi=300, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    main()