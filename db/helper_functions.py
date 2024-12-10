import pandas as pd

big_list_path = "./data/csv/updated.csv"
modulus_path = "./data/csvNewSwiftSNweblist.csv"


def csv_to_dataframe(file_path: str, cols: list[str]) -> pd.DataFrame:
    """
    Read a CSV file and isolate the columns of interest
    :param file_path: str: path to the CSV file
    :param cols: list[str]: list of column names to isolate
    :return: pd.DataFrame: dataframe with only the columns of interest
    """

    df = pd.read_csv(file_path)
    df = df[cols]
    return df


def create_master_csv() -> None:
    """
    Create a master CSV file from the big list and modulus CSV files
    """

    df1 = csv_to_dataframe(big_list_path, ["name", "type", "redshift"])
    df2 = csv_to_dataframe(modulus_path, ["SNname", "Distance_best"])

    df1["df1_name_lower"] = df1["name"].str.lower()
    df2["df2_name_lower"] = df2["SNname"].str.lower()

    df = df1.merge(df2, how="left", left_on="df1_name_lower", right_on="df2_name_lower", suffixes=("", "_y"))
    df = df.drop(columns=["df1_name_lower", "df2_name_lower", "SNname"])
    df["modulus"] = df["Distance_best"]
    df = df.drop(columns=["Distance_best"])

    df.to_csv("./data/csvmaster.csv", index=False)
    print("Master CSV created.")
