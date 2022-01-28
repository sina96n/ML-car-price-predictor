import pandas as pd


cars = pd.read_csv("cars.csv")
cars.head(3)


cars["Year"] = cars.Name.str.extract("(\d\d\d\d)" , expand=False).astype(int)
cars["Name"] = cars.Name.str.replace("(\d\d\d\d )", "", regex=True)

cars["Brand"] = cars.Name.str.extract("([\w]+)" , expand=False)
cars["Brand"] = cars["Brand"].apply(lambda x : x.strip())

cars["Name"] = cars.Name.str.replace("(^[\w]+ )", "",regex=True)
cars["Name"] = cars.Name.apply(lambda x : x.strip())

cars["Engine V"] = cars.Engine.str.extract("(\d\.*\d*)").astype(float)
cars["Engine"] = cars.Engine.str.replace("(\d\.*\d*L )", "", regex=True)


cars = cars.dropna()

cars.to_csv(
    "cleaned_data.csv", 
    index=False
)

# By Sina Kazemi
# Github : https://github.com/sina96n/