import click
import os
import pandas as pd
import pingouin as pg
import pickle
import matplotlib.pyplot as plt


@click.command()

@click.option('--cleaned-data', 'cleaned_data', type=click.Path(exists=True),
              default="data/processed/clean_diabetes.csv", help="Path to read in cleaned data")

@click.option('--model', 'model', type = click.Path(exists=True),
              default = 'results/models/lr_model.pickle', help="Path to read in model")

@click.option('--plot-output', 'plot_output', type = click.Path(exists=True),
              default = 'results/figures', help='Directory plots will be output to')

@click.option('--table-output', 'table_output', type = click.Path(exists=True),
              default = 'results/tables', help = 'Directory tables will be output to')

def main(cleaned_data, model, plot_output, table_output):
    '''
    Creates and saves model diagnostic output.

    Saves a .csv of Shapiro-Wilk test results. 
    Saves .pngs of a qqplot and scatterplot of the model's residuals.
    '''

    diabetes_df = pd.read_csv(cleaned_data)

    y = diabetes_df["C_peptide"]

    with open(os.path.join(model), "rb") as f:
        model = pickle.load(f)

    resid = model["residuals"]

    # Shapiro-Wilk test
    shapiro_test = pg.normality(resid, method="shapiro") 

    with open(os.path.join(table_output, "shapiro_wilk.csv"), "w") as f:

        f.write(shapiro_test.round(3).to_csv())

    # Q-Q plot
    pg.qqplot(resid)
    plot_path = os.path.join(plot_output, "qq_plot.png")
    plt.savefig(plot_path, dpi=300, bbox_inches="tight")
    plt.close()

    fitted_df = pd.DataFrame({
        "fitted": y - resid,
        "residuals": resid
        })

    # residual plot
    # converted from altair to matplotlib with Claude Sonnet 4.5
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(fitted_df["fitted"], fitted_df["residuals"], alpha=0.6)
    ax.axhline(y=0, color='red', linestyle='--', linewidth=1.5)
    ax.set_xlabel("Fitted Values")
    ax.set_ylabel("Residuals")
    plot_path = os.path.join(plot_output, "resid_plot.png")
    plt.savefig(plot_path, dpi=300, bbox_inches="tight")
    plt.close()



if __name__ == "__main__":
    main()