Data Science test Plutus Research Pvt Ltd
  
Understanding the data:
1) Any file contains market data for a security for a day.
2) The data is in following format:
        Column 1 - Date
        Column 2 - Time instant(in seconds)
        Column 3 - Bid price(at a particular time instant)
        Column 4 - Ask price(at a particular time instant)
        Column 5 - A notion of market weighted price(this may considered as a
        fair price at the time instant)
        Column 6:end - features
3) It should be noted that the features start only from column 6 to the last
column

Parameter file for linear models:
1) The parameter file need to contain weights of the features and the threshold
for placing an order.
2) Weights should be mentioned starting with "WEIGHTS:" followed by n "," separated
doubles, n being the number of features in the data
3) Threshold should be mentioned starting with "THRESHOLD:" followed by a
double

	Sample parameter file for linear model:
	WEIGHTS: 1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00
	THRESHOLD: 200.00

Non linear models:
In case of non linear models the file model.py needs to be modified. One may
add more parameters in param_file, but support needs to be added in model.py
for the same.

Scoring Criteria:
1) Overall the assessment will be both on the approach as well as the PNL
score obtained. Even a negative PNL score with a good approach may be
considered.
2) The score shall be judged on three criteria PNL Sharpe, absolute PNL and
the trade count.
3) The PNL profile may vary according to the trade one is targeting and so
the above score would be judged according the trade being targeted.
4) The score computed will be on a separate test data which will not be shared
with the candidates.

Generating the PNL score:
Script - ./read_params_and_simulate.py <paramfile> <datalocation>
Sample command - ./read_params_and_simulate.py sample_param data/P1/

Understanding the output:
The output contains each day's PNL, minimum PNL, trades done and end of day
positions. It also contains the statistics across days like average PNL,
Sharpe of PNL and average traded volume per day.

Note:
1) As for any data science problem one should try to predict the price here and
not use the features from the future in the process.
2) A proper estimate of fitting(underfitting/overfitting) may be required to
do good in test set.
3) The modification are only allowed in model.py and not in read_params_and_simulate.py

Submissions to be made:
1) model.py(if modified)
2) param file
3) writeup, elaborating each and every step
