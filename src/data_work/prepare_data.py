import argparse
import pandas as pd
import numpy as np


def import_raw_data(year:int=2024) -> np.array:
        
    down_value_str = str(year-1)
    up_value_str = str(year)

    importing_string = "data/raw_data/rs_"+down_value_str+"_"+up_value_str+".csv"
    importing_string_advance = "data/raw_data/rs_"+down_value_str+"_"+up_value_str+"_advanced.csv"

    data = pd.read_csv(importing_string)
    data_advance = pd.read_csv(importing_string_advance)
    result = pd.concat([data, data_advance], axis='columns')   

    return result.drop_duplicates()


def main():

    parser = argparse.ArgumentParser(description="Importowanie data from different years")
    parser.add_argument("--start_year", type=int, default=1999, help="Starting year")
    parser.add_argument("--end_year", type=int, default=2024, help="Ending year")
    args = parser.parse_args()
    
    start_year = args.start_year
    end_year = args.end_year

    while end_year > start_year:
        data = import_raw_data(end_year)
        np.save("data/redacted_data/rs_"+str(end_year-1)+"_"+str(end_year)+"_full", data)
        end_year -= 1

if __name__ == '__main__':
    main()