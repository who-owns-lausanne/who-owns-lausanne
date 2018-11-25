import pandas as pd

proprio = pd.read_json('proprio.json')

# drop fields missing commune number
proprio = proprio[~proprio['numcom'].isna()]

# only select parcelles in the commune of Lausanne
proprio_lauz = proprio.query('numcom == 132')

# very few rows are missing the proprietary. drop them
proprio_lauz = proprio_lauz[~proprio_lauz['proprio'].isna()]

#drop duplicate rows (caused by overlap of rectangles during scraping)
proprio_lauz = proprio_lauz.drop_duplicates()

# cast to the proper dtypes
proprio_lauz = proprio_lauz.astype({'numcom':pd.np.int, 'no_parc':pd.np.int})

# serialize to csv
proprio_lauz.to_csv('proprio_lausanne.csv', index=False)
