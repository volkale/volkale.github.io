import numpy as np
import pandas as pd
from datetime import date, timedelta
from scipy import stats
import pystan
import matplotlib.pyplot as plt

#########################
#### Data Simulation ####
#########################

def get_data(p, pi, lambda_, days, data_per_day, end_date):
    np.random.seed(321)
    data = []

    conversion = np.random.binomial(1, p, size=days * data_per_day)
    zero_infl = np.random.binomial(1, pi, size=days * data_per_day)
    geom = np.random.geometric(p=lambda_, size=days * data_per_day) - 1

    i = 0
    for d in range(days):
        for _ in range(data_per_day):
            is_conv = conversion[i]
            if is_conv == 0:
                lag = -1
            else:
                lag = 0 if zero_infl[i] == 1 else geom[i]

            elapsed_days = days - d - 1
            data.append([is_conv, lag, elapsed_days])
            i += 1

    sim = pd.DataFrame(data, columns=['conv', 'lag', 'elapsed'])
    sim['frequency'] = 1

    sim = sim.groupby(['conv', 'lag', 'elapsed']).agg('sum').reset_index()
    
    sim['visit_date'] = sim['elapsed'].map(lambda x: end_date - timedelta(x))

    sim['conversion_date'] = sim[['visit_date', 'lag']] \
        .apply(
            lambda x: x[0]+timedelta(x[1]) \
            if x[1] >= 0
            else None,
            axis=1
        )

    return sim


# simulate test and control data for 28 days
end_date = date(2022, 2, 28)
days = 42
start_date = end_date - timedelta(days-1)
data_per_day = 5000

# model parameters for the simulation
p_t, pi_t, lambda_t = 0.05, 0.6, 0.6
p_c, pi_c, lambda_c = 0.06, 0.2, 0.2

# get the simulated data
sim_t = get_data(p_t, pi_t, lambda_t, days, data_per_day, end_date)
sim_c = get_data(p_c, pi_c, lambda_c, days, data_per_day, end_date)
sim_c['is_control'] = 1
sim_t['is_control'] = 0 
sim = pd.concat([sim_c, sim_t])
sim = sim.sort_values(['is_control', 'visit_date', 'conversion_date']).reset_index()[['is_control', 'visit_date', 'conversion_date', 'frequency']]


# simulate only testing for d days only with d=1,..., 28
stats_series = []
for d in range(1, days + 1):

    # cutoff date := last observed day of test
    cutoff_date = start_date + timedelta(d - 1)

    tmp = sim.copy()
    
    # conversions after cut off date are not observed
    tmp['conversion_date'] = tmp['conversion_date'] \
    .map(
        lambda x: x
        if x is None or (cutoff_date - x).days >= 0 \
        else None
    )
    
    tmp['has_conversion'] = tmp['conversion_date'].map(lambda x: int(x is not None))
    
    tmp = tmp[tmp.visit_date <= cutoff_date]
        
    # get odds ratio and pvalues for data set
    data = tmp.groupby(['is_control', 'has_conversion']).agg({'frequency': sum}).unstack(0).iloc[::-1].values
    or_pval = stats.fisher_exact(data)
    stats_series.append([d, *or_pval])

# define summary dataframe
res = pd.DataFrame(stats_series, columns=['test days', 'odds ratio', 'Fisher\'s p-val'])
res['odds ratio'] = res['odds ratio'].round(2)
res['stat. sign. at 5%'] = res['Fisher\'s p-val'].astype(float) < 0.05
res['Fisher\'s p-val'] = res['Fisher\'s p-val'].map(lambda x: '{:0.1e}'.format(x))


# plot summary
fig, ax = plt.subplots(figsize=(10,4))
_ = res[(res['stat. sign. at 5%']) & (res['odds ratio']>1)].plot.scatter(
    x='test days', y='odds ratio', ax=ax, color='green', marker='^', label='reject null'
)
_ = res[~res['stat. sign. at 5%']].plot.scatter(
    x='test days', y='odds ratio', ax=ax, color='k', marker='D', label='fail to reject null'
)
_ = res[(res['stat. sign. at 5%']) & (res['odds ratio']<1)].plot.scatter(
    x='test days', y='odds ratio', ax=ax, color='red', marker='v', label='reject null'
)
_ = ax.hlines(p_t / p_c, 0, days, linestyle='--', label='true odds ratio')
_ = ax.legend()
_ = ax.set_ylim(0.6, 2.4)
fig.savefig('results_by_test_days.png')

#################################################
#################################################

# Larry's 7 day test analysis

cutoff_date = start_date + timedelta(6)

tmp = sim.copy()
tmp['conversion_date'] = tmp['conversion_date'] \
.map(
    lambda x: x
    if x is None or (cutoff_date - x).days >= 0 \
    else None
)
tmp['has_conversion'] = tmp['conversion_date'].map(lambda x: int(x is not None))
tmp = tmp[tmp.visit_date <= cutoff_date]

# Fisher's exact test
data = tmp.groupby(['is_control', 'has_conversion']).agg({'frequency': sum}).unstack(0).iloc[::-1].values
pval = stats.fisher_exact(data)[1]
# print p value
print(pval)


# Bayesian analysis

# save stan model from here https://github.com/volkale/convpybayes/blob/main/src/stan/disconvpy.stan in a file named disconvpy.stan and add it to the same directory

# compile stan model
sm = pystan.StanModel(file='disconvpy.stan')

# fit models for test and control separately
fits = {}
for i in [0, 1]:
    tmp_i = tmp.query(f'is_control=={i}')
    
    cens_condition = tmp_i.conversion_date.isnull()
    obs_condition = tmp_i.conversion_date.notnull()

    N_cens = cens_condition.astype(int).sum()
    N_obs = obs_condition.astype(int).sum()

    data = dict(
        run_estimation=1,
        N_obs=N_obs,
        N_cens=N_cens,
        W_obs=tmp_i[obs_condition].frequency.values,
        W_cens=tmp_i[cens_condition].frequency.values,
        conv_lag_obs=(tmp_i[obs_condition].conversion_date - tmp_i[obs_condition].visit_date).dt.days,
        elapsed_time=(cutoff_date - tmp_i[cens_condition].visit_date).dt.days
    )

    fit = sm.sampling(data=data)
    
    fits[i] = fit


# plot posterior of p
fig, ax = plt.subplots(figsize=(10, 4))
_ = ax.hist(fits[1].extract()['p'], bins=100, alpha=0.5, label='control', density=True)
_ = ax.hist(fits[0].extract()['p'], bins=100, alpha=0.5, label='test', density=True)
_ = ax.set_yticklabels([])
_ = ax.legend()
fig.savefig('posteriorCVR.png')
