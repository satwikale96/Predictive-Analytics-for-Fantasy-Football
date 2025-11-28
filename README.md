# Predictive Analytics for the Fantasy Football Draft

### Description:

Using this repo, the user will gather a variety of data sources dating from 2010 to 2021 containing player historical fantasy performance, average draft positions, team strength of schedule, and more. 
Once the data is gathered, the additional code will transform the weekly data and other scraped sources into one annual data source for model training, testing, and 2022 predictions. 
Lastly, with the predictions completed, the data is then organized for Tableau reporting.

### Installation:

1. In order to install and setup the code, the user will first need to download the included Python and IPYNB files. Next, the user will need to ensure that they have Pandas, Numpy, and Scikit-learn installed in their python environment.

### Execution:

1. With the environment prepared and files downloaded, the user must begin by running the following Data Gathering python file: "data_gather.py". This file will import all of the included python scraping files, run them, and output a dataset at the weekly level.
2. The next step in the process is running the "Gathering and Preprocessing.ipynb" file. This code takes the weekly level data from 2010-2021 and aggregates it at the yearly level to preprocess the statistics and measures necessary for modeling.
3. Once the data has been converted to the annual level, the user will run "Pivot_data.ipynb" to prepare the dataset for training in the shape of the following: Response: Year - 0 Fantasy Points. Predictors: Year - 1, Year -2, and year - 3.
4. To train the models and return their performance on the test and 2021 sets, the user will run "Modeling.ipynb" which saves model results, 2021 predictions, and 2022 predictions for each position. The user will then use these to select the optimal model.
5. With the optimal model determined, the user will run "Organize_Predictions.ipynb" to organize the 2021 predictions for comparing to the experts (ESPN and FantasyNerds) as well as organize the 2022 predictions for Tableau.
6. Next, the user will run "Comparing_To_Experts.ipynb" for calculating the Cumulative Discounted Metric for the model's predicted rankings, ESPN's rankings, and FantasyNerds rankings. 
7. Lastly, the user will utilize the "2022_Predictions.xlsx" file to upload into the attached Tableau packaged workbook for leveraging during the 2022 Fantasy Football draft. 
