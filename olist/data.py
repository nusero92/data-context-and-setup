import os
import pandas as pd
import glob


class Olist:
    def get_data(self):
        """
        This function returns a Python dict.
        Its keys should be 'sellers', 'orders', 'order_items' etc...
        Its values should be pandas.DataFrames loaded from csv files
        """
        # Hints 1: Build csv_path as "absolute path" in order to call this method from anywhere.
            # Do not hardcode your path as it only works on your machine ('Users/username/code...')
            # Use __file__ instead as an absolute path anchor independant of your usename
            # Make extensive use of `breakpoint()` to investigate what `__file__` variable is really
        # Hint 2: Use os.path library to construct path independent of Mac vs. Unix vs. Windows specificities
        csv_path=os.path.realpath('/home/ana/code/nusero92/data-context-and-setup/data/csv')

        df=[]
        filename=glob.glob(csv_path+ "/*.csv")
        for file in filename:
            df.append(pd.read_csv(file))

        file_names=os.listdir(csv_path)
        file_names.remove(".keep")

        key_names=[]
        for names in file_names:
            key_names.append(names.replace("olist_","").replace("_dataset.csv", "").replace(".csv", ""))

        data=dict(zip(key_names, df))
        return data



    def ping(self):
        """
        You call ping I print pong.
        """
        print("pong")
