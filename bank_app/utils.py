import pandas as pd
import numpy as np
import pickle

def process(df):
	df.job = df.job.apply(lambda x: 'admin' if x=='admin.' else x)
	df.job = df.job.apply(lambda x: 'management' if x=='mgmt' else x)
	# check if job has right columns

	df.default = df.default.apply(lambda x: 0 if x=='no' else 1)
	df.housing = df.housing.apply(lambda x: 0 if x=='no' else 1)
	df.loan = df.loan.apply(lambda x: 0 if x=='no' else 1)
	df.y = df.y.apply(lambda x: 0 if x=='no' else 1)

	months = np.array(['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'])
	df.month = df.month.apply(lambda x: np.where(months==x)[0][0])

	df['pdays_0_70'] = [1 if (i>-1 and i <=70) else 0 for i in df.pdays]
	df['pdays_70_110'] = [1 if (i >70 and i<=110) else 0 for i in df.pdays]
	df['pdays_110_160'] = [1 if (i >110 and i<=160) else 0 for i in df.pdays]
	df['pdays_160_210'] = [1 if (i >160 and i<=210) else 0 for i in df.pdays]
	df['pdays_210_380'] = [1 if (i >210 and i<=380) else 0 for i in df.pdays]
	df['pdays_380'] = [1 if (i >380) else 0 for i in df.pdays]
	df = df.drop(columns=['pdays'])

	for col in ['job_admin', 'job_blue-collar', 'job_entrepreneur', 'job_housemaid',
	       'job_management', 'job_retired', 'job_self-employed', 'job_services',
	       'job_student', 'job_technician', 'job_unemployed', 'marital_divorced',
	       'marital_married', 'marital_single', 'education_primary',
	       'education_secondary', 'education_tertiary', 'contact_cellular',
	       'contact_telephone', 'poutcome_failure', 'poutcome_other',
	       'poutcome_success']:
	    df[col] = df[col.split('_')[0]].apply(lambda x: 1 if x==col.split('_')[1] else 0)

	for col in ['job','marital','education','contact','poutcome']:
		if col in df.columns:
			df = df.drop(columns=[col])
	# df = df.drop(columns=['job','marital','education','contact','poutcome'])

	X = df.drop(columns=['y'])
	Y = df.y

	file = open('models/rfmod.pkl', 'rb')
	rfmodel = pickle.load(file)

	acc = rfmodel.score(X,Y)

	return np.round(acc*100, 2)