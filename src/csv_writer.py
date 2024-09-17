import pandas as pd

class CSV_Writer():
    def __init__(self, file: str):
        if file[len(file) - 4:] != ".csv":
            print("This is not a csv file!")
        else:
            self.file = file

    def write(self, df: pd.DataFrame, conditions: list=None):
        if conditions == None:
            df.to_csv(self.file, index=False)
        else:
            df = df[conditions].copy()
            df.to_csv(self.file, index=False)
    
    def get_file(self) -> str:
        return self.file
    
    def set_file(self, file: str):
        if file[len(file) - 4:] != ".csv":
            print("This is not a csv file!")
        else:
            self.file = file