
# Librairy imports 
import pandas as pd
import plotly.express as px
import numpy as np 
import plotly.graph_objects as go
from os import listdir
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent='dhraief')

PATH = "/data"
def find_csv_filenames( path_to_dir, suffix=".csv" ):
    """ Returns a list of files ending with suffis in the path """
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]

def create_df():
    """ Returns a concatenated version of all wars"""
    files_names =find_csv_filenames(PATH)
    data = pd.read_csv("data/"+files_names[0])
    for idx,name in enumerate(files_names[1:]):
    data = pd.concat([data,pd.read_csv("data/"+name)]) 
    
def cleaning_df(data):
    data.columns = data.iloc[0]
    data.drop(0,axis=0,inplace=True)
    data.drop(data.columns[-3:],axis=1,inplace=True)
    data.reset_index(inplace=True)
    data.drop(data.columns[0],axis=1,inplace=True)
    data.rename(columns={"Victorious party (if applicable)":"Victorious","Defeated party (if applicable)":"Defeated"},inplace=True)

def name_pre_process(data):
    """ Create a list from Victorious and Defeated columns and then explode the colums """
    data.Victorious = data.Victorious.apply(lambda x:str(x).split("\n"))
    data.Defeated = data.Defeated.apply(lambda x:str(x).split("\n"))
    data = data.explode("Victorious",ignore_index=True)
    data = data.explode("Defeated")

def add_coord(data,countries):
    def get_coord(country:str):
        """ returns (lat,lon) tuple from country name
        """
        try:
            if geolocator.geocode(country) is None:
                print(country +"None" )
                return None
            raw = geolocator.geocode(country).raw
            return (raw["lat"],raw["lon"])
        except:
            return None
    data_with_coord = data.merge(countries,left_on="Victorious",right_on="Country",how="left")
    data_with_coord.rename({"lat":"lat_vic","lon":"lon_vic"},inplace=True,axis=1)
    data_with_coord = data_with_coord.merge(countries,left_on="Defeated",right_on="Country",how="left")
    data_with_coord.dropna(inplace=True)
    data_with_coord.drop(["Country_def","Country"],inplace=True,axis=1)
    return data_with_coord 

def explode_period(df):
    """ Transforms the Started-ended into multiple rows with every year of the conflict """
    def adjust_type(df):
        """ Does some data cleaning"""
        df.Started = df.Started.astype(int)
        df.Ended.replace({"Ongoing":2022},inplace=True)
        df.Ended = df.Ended.astype(int)
        
    def generate_dict(df):
        """ Generate a dict that maps every year to the conflicts it had"""
        min_year = min(df.Started)
        max_year = max(df.Ended)
        year_war = {}
        for y in range(min_year,max_year+1):
            year_war[y] = []
        for start,end,idx in zip(df.Started,df.Ended,df.index):
            for year in range(start,end+1):
                year_war[year].append(idx)
        return year_war
        
    adjust_type(df)
    year_war = generate_dict(df)    
    year_war_df = pd.DataFrame({"year":year_war.keys(),"war_idx":year_war.values()})
    year_war_df = year_war_df.explode("war_idx")
    return year_war_df.merge(df,left_on="war_idx",right_on=df.index)

def main():
    data = create_df()
    cleaning_df(data)
    name_pre_process(data)
    countries = pd.concat([data.Victorious,data.Defeated]).unique()
    data = add_coord(data,countries)
    data = explode_period(data)
    data.to_csv("full_countries_with_coord.csv")
if __name__ == "__main__":
    main()
