""" Outputs a list of top 300 subscription apps that had the best
rank over the past 365 days.
"""
import pickle
import pandas as pd
import matplotlib.pyplot as plot 

__author__ = 'SONIYA RODE'


def readfiles():
	"""
	Retrieves pickled data from files.
	:return : info and rank dataframes
	"""
	with open('app_info_df.pkl','rb')as f1 ,open('app_rank_df.pkl','rb')  as f2 :
		#infoDf: App info dataframe
		infoDf=pickle.load(f1)
		#rankDf: App rank dataframe
		rankDf=pickle.load(f2)
	return infoDf,rankDf

def preporcessInfo(infoDf):
	"""
	Filter outs subscription apps by looking for keywords:subscription,renewal,subscribe
	in the app 'description' field
	:param infoDf(dataframe): Dataframe containing all apps. 
	:return infoDf(dataframe): Dataframe containing subscription apps. 
	"""
	searchFor=['subscription','subscribe','renewal']
	infoDf=infoDf[infoDf['description'].str.contains('|'.join(searchFor))]
	return infoDf

def preprocessingRank(rankDf):
	"""
	The function forward fill the last available if there's no valid rank data for a 
	certain date present. If there’s no historical data sets 300 as default rank.
	:param rankDf(dataframe): Dataframe containing ranks of apps overtime.
 	:return rankDf(dataframe): Dataframe with forward fill and default ranks set.
	"""

	#forward fill the rank data rowwise 
	rankDf.fillna(method='ffill', axis=1, inplace=True)
	
	#If there’s no historical data sets 300 as default rank
	rankDf.fillna(value=300, inplace=True)

	return rankDf

if __name__ == '__main__':

	
	#Retrieve pickled data
	infoDf,rankDf=readfiles()

	#Get all the subscription apps
	infoDf=preporcessInfo(infoDf)

	#Preprocess rank df to replace NAN with forward fill and set default =300
	rankDf=preprocessingRank(rankDf)
	
	#Calculate mean rank of each app
	rankDf['mean_rank']=rankDf.mean(axis=1)

	#Remove app rank by date columns, keep mean_rank column
	rankDf.drop(rankDf.iloc[:, :849], inplace = True, axis = 1) 
	
	#Perform merge operation to get subscription apps and their ranks
	subscriptionApps=pd.merge(infoDf,rankDf,on='itunes_app_id')
	
	#Sort subscription apps according to mean_rank
	subscriptionApps.sort_values(by=['mean_rank'],ascending = False,inplace=True)

	#Write top 300 subscritption apps details to csv
	subscriptionApps.head(300).to_csv('Top300subscriptionApps.csv')
