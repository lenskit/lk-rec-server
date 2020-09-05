#!/usr/bin/env python
# coding: utf-8

# In[65]:


import asyncio
import aiohttp
import json
import sqlite3
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import urllib
from pandas.io import sql
from datetime import datetime
import numpy as np
import requests
from time import perf_counter 


# # Performance Testing

# In[3]:


class ConfigReader:
    def get_value(self, key):
        with open('config.json') as json_data_file:
            data = json.load(json_data_file)
        return data[key]


# In[59]:


class DbManager:
    def __init__(self):
        reader = ConfigReader()
        db_connection = reader.get_value("db_connection")        
        self.conn_string = '{db_engine}{connector}://{user}:{password}@{server}/{database}'.format(
            db_engine=db_connection['db_engine'],
            connector=db_connection['connector'],
            user=db_connection['user'],
            password=db_connection['password'],
            server=db_connection['server'],
            database=db_connection['database'])

    def get_users(self):
        return sql.read_sql("SELECT distinct userId FROM ratings;", create_engine(self.conn_string))


# ## Get random users

# In[61]:


n_rand_users = 1000
dbManager = DbManager()
db_users = dbManager.get_users()
n_rand_users = db_users.sample(n=n_rand_users)


# ## Test recommendation endpoint

# In[62]:


base_url = 'http://127.0.0.1:8000'
algo_rec = 'popular'
algo_pred = 'biasedmf'
n_recs = 5
items = "10,20,30,40,50"


# ### Parallel performance

# In[67]:


def print_stats(times, time_taken_all, num_requests):
    print(f'Total response time: {time_taken_all}')
#   print(f'Average load time: {time_taken_all / num_requests}')
    print(f'Mean response time: {np.mean(times)}')
    print(f'99 percentile: {np.quantile(times, 0.99)}')
    print(f'Throughput (requests per second): {num_requests / time_taken_all}')
    print(f'Peak response time: {max(times)}')
    
async def get_recs():
    times = []
    num_requests = len(n_rand_users)
    print(f'Number of requests: {num_requests}')
    start_recs = perf_counter()
    for idx, row in n_rand_users.iterrows():
        start = perf_counter()
        await get_user_results(row['userId'], n_recs, algo_rec, None)
        time_taken = perf_counter() - start
        times.append(time_taken)
#        print(f'Response time: {time_taken}')
    time_taken_all = perf_counter() - start_recs
    print_stats(times, time_taken_all, num_requests)

async def get_preds():
    times = []
    start_preds = perf_counter()
    num_requests = len(n_rand_users)
    print(f'Number of requests: {num_requests}')    
    for idx, row in n_rand_users.iterrows():
        start = perf_counter()
        await get_user_results(row['userId'], None, algo_pred, items)
        time_taken = perf_counter() - start
        times.append(time_taken)
#        print(f'Response time: {time_taken}')
    time_taken_all = perf_counter() - start_preds
    print_stats(times, time_taken_all, num_requests)
    
async def get_user_results(userId, nr_recs, algo, items):
    is_a_rec_request = True if algo == 'popular' or algo == 'topn' else False
    if is_a_rec_request:
        url = f'{base_url}/algorithms/{algo}/recommendations?user_id={userId}&num_recs={nr_recs}'
    else:
        url = f'{base_url}/algorithms/{algo}/predictions?user_id={userId}&items={items}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()


# In[68]:
print('-------------------------------------')
print('Predictions results')
loop = asyncio.get_event_loop()
loop.run_until_complete(get_preds())

# In[42]:

print('-------------------------------------')
print('Recomendation results')
loop = asyncio.get_event_loop()
loop.run_until_complete(get_recs())
loop.close()


# ### Single thread performance

# In[69]:


def print_stats_single_thread(times, time_taken_all, num_requests):
    print(f'Total response time: {time_taken_all}')
#   print(f'Average load time: {time_taken_all / num_requests}')
    print(f'Mean response time: {np.mean(times)}')
    print(f'99 percentile: {np.quantile(times, 0.99)}')
    print(f'Throughput (requests per second): {num_requests / time_taken_all}')
    print(f'Peak response time: {max(times)}')
    
def get_recs_single_thread():
    times = []
    num_requests = len(n_rand_users)
    print(f'Number of requests: {num_requests}')
    start_recs = perf_counter()
    for idx, row in n_rand_users.iterrows():
        start = perf_counter()
        get_user_results_single_thread(row['userId'], n_recs, algo_rec, None)
        time_taken = perf_counter() - start
        times.append(time_taken)
#        print(f'Response time: {time_taken}')
    time_taken_all = perf_counter() - start_recs
    print_stats_single_thread(times, time_taken_all, num_requests)

def get_preds_single_thread():
    times = []
    start_preds = perf_counter()
    num_requests = len(n_rand_users)
    print(f'Number of requests: {num_requests}')    
    for idx, row in n_rand_users.iterrows():
        start = perf_counter()
        get_user_results_single_thread(row['userId'], None, algo_pred, items)
        time_taken = perf_counter() - start
        times.append(time_taken)
#        print(f'Response time: {time_taken}')
    time_taken_all = perf_counter() - start_preds
    print_stats_single_thread(times, time_taken_all, num_requests)
    
def get_user_results_single_thread(userId, nr_recs, algo, items):
    is_a_rec_request = True if algo == 'popular' or algo == 'topn' else False
    if is_a_rec_request:
        url = f'{base_url}/algorithms/{algo}/recommendations?user_id={userId}&num_recs={nr_recs}'
    else:
        url = f'{base_url}/algorithms/{algo}/predictions?user_id={userId}&items={items}'

    r = requests.get(url)
    data = r.json()


# In[70]:

print('-------------------------------------')
print('Predictions results in single thread')
get_preds_single_thread()


# In[51]:

print('-------------------------------------')
print('Recommendations results in single thread')
get_recs_single_thread()


# In[ ]:




