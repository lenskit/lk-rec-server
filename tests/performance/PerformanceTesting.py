#!/usr/bin/env python
# coding: utf-8

# In[1]:


# %pip install aiohttp
# %pip install mysql-connector-python
# %pip install nest_asyncio
# %pip install lenskit --upgrade
# %pip install psycopg2


# In[17]:


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
# import matplotlib.pyplot as plt
# import seaborn as sns
import pandas as pd
# import nest_asyncio
# nest_asyncio.apply()


# # Performance Testing

# In[5]:


class ConfigReader:
    def get_value(self, key):
        with open('config.json') as json_data_file:
            data = json.load(json_data_file)
        return data[key]


# In[6]:


class DbManager:
    def __init__(self):
        reader = ConfigReader()
        db_connection = reader.get_value("db_connection")        
        self.conn_string = '{db_engine}{connector}://{user}:{password}@{server}/{database}?port={port}'.format(
            db_engine=db_connection['db_engine'],
            connector=db_connection['connector'],
            user=db_connection['user'],
            password=db_connection['password'],
            server=db_connection['server'],
            database=db_connection['database'],
            port=db_connection['port'])

    def get_users(self):
        # postgres:
#        return sql.read_sql("SELECT distinct \"user\" FROM rating;", create_engine(self.conn_string))
        # mysql:
        return sql.read_sql("SELECT distinct user FROM rating;", create_engine(self.conn_string))


# ## Test recommendation endpoint

# ### Semaphore performance

# In[7]:


import os
throughputs = []

def print_stats(times, time_taken_all, num_requests):
    print(f'Total response time: {round(time_taken_all, 3)}')
    print(f'Throughput (requests per second): {round(num_requests / time_taken_all, 3)}')
    print(f'Peak response time: {round(max(times), 3)}')
    print(f'Mean response time: {round(np.mean(times), 3)}')
    print(f'99 percentile: {round(np.quantile(times, 0.99), 3)}')

def plot_numbers(file_name):
    resp_time_per_request = np.genfromtxt(file_name, delimiter=',')
    plt.plot(resp_time_per_request)
    plt.show()
    
def hist_numbers(file_name):
    resp_time_per_request = np.genfromtxt(file_name, delimiter=',')
    plt.hist(resp_time_per_request, bins='auto')
    plt.show()

# Predictions    
async def get_preds_sem(num_sem, algo_pred, file_name=None, add_throughput=False):
    times = []
    sem = asyncio.Semaphore(num_sem)
    tasks = []    
    num_requests = len(n_rand_users)
    print(f'Number of requests: {num_requests}')
    start_preds = perf_counter()

    async with aiohttp.ClientSession() as session:
        for idx, row in n_rand_users.iterrows():
            task = asyncio.ensure_future(get_user_preds_with_sem(row['user'], algo_pred, items, session, sem, times))
            tasks.append(task)         

        responses = await asyncio.gather(*tasks)
        time_taken_all = perf_counter() - start_preds
        print_stats(times, time_taken_all, num_requests)
        
        if file_name != None and file_name != '':
            if os.path.exists(file_name):
                os.remove(file_name)
            np.savetxt(file_name, times, delimiter=',')
        
        if add_throughput:
            throughputs.append(num_requests / time_taken_all)

async def get_user_preds_with_sem(user, algo, items, session, sem, times):
    async with sem:  # semaphore limits num of simultaneous downloads
        return await get_user_preds_sem(user, algo, items, session, times)        
        
async def get_user_preds_sem(user, algo, items, session, times):
    url = f'{base_url}/algorithms/{algo}/predictions?user_id={user}&items={items}'
    start = perf_counter()
    async with session.get(url) as resp:
        data = await resp.json()    
        time_taken = perf_counter() - start
        times.append(time_taken)
        
# Recommendations
async def get_recs_sem(num_sem, algo_rec, file_name=None, add_throughput=False):
    times = []
    sem = asyncio.Semaphore(num_sem)
    tasks = []
    num_requests = len(n_rand_users)
    print(f'Number of requests: {num_requests}')
    start_preds = perf_counter()

    async with aiohttp.ClientSession() as session:
        for idx, row in n_rand_users.iterrows():
            task = asyncio.ensure_future(get_user_recs_with_sem(row['user'], algo_rec, n_recs, session, sem, times))
            tasks.append(task)         

        responses = await asyncio.gather(*tasks)
        time_taken_all = perf_counter() - start_preds
        print_stats(times, time_taken_all, num_requests)
        
        if file_name != None and file_name != '':
            if os.path.exists(file_name):
                os.remove(file_name)
            np.savetxt(file_name, times, delimiter=',')
        
        if add_throughput:
            throughputs.append(num_requests / time_taken_all)

async def get_user_recs_with_sem(user, algo, n_recs, session, sem, times):
    async with sem:  # semaphore limits num of simultaneous downloads
        return await get_user_preds_sem(user, algo, n_recs, session, times)        
        
async def get_user_recs_sem(user, algo, n_recs, session, times):
    url = f'{base_url}/algorithms/{algo}/recommendations?user_id={user}&num_recs={n_recs}'
    start = perf_counter()
    async with session.get(url) as resp:
        data = await resp.json()    
        time_taken = perf_counter() - start
        times.append(time_taken)   


# ### Gunicorn methods

# In[8]:


import subprocess
import os

def get_gunicorn_master_pid():
    proc1 = subprocess.Popen(['ps', 'ax'], stdout=subprocess.PIPE)
    proc2 = subprocess.Popen(['grep', 'gunicorn'], stdin=proc1.stdout,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    proc1.stdout.close() # Allow proc1 to receive a SIGPIPE if proc2 exits.
    out, err = proc2.communicate()
    process_length = ConfigReader().get_value('process_length')
    master_id = out[:process_length].decode('utf-8').replace(' ', '')
    return master_id

def add_workers(n):
    master_id = get_gunicorn_master_pid()
    for i in range(n):
        os.system(f"kill -s TTIN {master_id}")
        
def remove_workers(n):
    master_id = get_gunicorn_master_pid()
    for i in range(n):
        os.system(f"kill -s TTOU {master_id}")    


# ### Get random users

# In[9]:


reader = ConfigReader()
n_rand_users = num_requests = reader.get_value("num_requests")
dbManager = DbManager()
db_users = dbManager.get_users()
n_rand_users = db_users.sample(n=n_rand_users)


# ### Get config values

# In[10]:


base_url = reader.get_value("rec_server_baese_url")
n_recs = reader.get_value("n_recs")
items = reader.get_value("items")
pred_algos = reader.get_value("pred_algos")
rec_algos = reader.get_value("rec_algos")


# ### Warm up phase

# In[19]:


async def warm_up_async(current_algo=None, num_workers=24, display_logs=True):
    warm_up_user = 1
    times = []
    tasks = []
    async with aiohttp.ClientSession() as session:
        for algo in pred_algos:
            if current_algo is None or algo == current_algo:
                for w in range(num_workers * 2):
                    if display_logs:
                        print(f'Calling {algo}. Worker number: {w + 1}')
                    task = asyncio.ensure_future(get_user_preds_sem(warm_up_user, algo, items, session, times))
                    tasks.append(task)
        responses = await asyncio.gather(*tasks)


# In[20]:


def warm_up(current_algo=None, num_workers=24, display_logs=True):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(warm_up_async(current_algo, num_workers, display_logs))
    loop.run_until_complete(future)


# In[21]:


warm_up(None, 4)


# ### Call predict and recommend from server for canonical config

# #### Predictions for different algorithms

# In[12]:


for algo in pred_algos:
    file_name = f'preds_{algo}_parallel_threads_8_workers_4_num_req_{num_requests}.csv'
    loop = asyncio.get_event_loop()
    print(f'Algorithm: {algo}')
    future = asyncio.ensure_future(get_preds_sem(8, algo, file_name, True))
    loop.run_until_complete(future)
#    plot_numbers(file_name)
#    hist_numbers(file_name)
    print('---------------------')
    print('')


# #### Recommendations

# In[13]:


algo_rec = 'popular'
print(f'Algorithm: {algo_rec}')
file_name = f'recs_{algo_rec}_parallel_threads_8_workers_4_num_req_{num_requests}.csv'
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(get_recs_sem(8, algo_rec, file_name))
loop.run_until_complete(future)
print('---------------------')
print('')
#plot_numbers(file_name)
#hist_numbers(file_name)


# ### Speedup Tests

# In[25]:


throughputs = []
linear_speedup_algos = reader.get_value("linear_speedup_algos")


# In[15]:


def call_server(file_name):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_preds_sem(8, current_algo, file_name, True))
    loop.run_until_complete(future)
#    plot_numbers(file_name)
#    hist_numbers(file_name)


# In[16]:


workers_config = reader.get_value("workers_config")
inc_config = reader.get_value("inc_config")


# In[17]:


for current_algo in linear_speedup_algos:
    i = 0
    throughputs = []
    remove_workers(3) # reduce from 4 workers to 1
    for num_workers in workers_config:
        print(f'Algo: {current_algo}, Workers: {num_workers}')
        warm_up(current_algo, num_workers, display_logs=False)
        file_name = f'preds_{current_algo}_parallel_threads_8_workers_{num_workers}_num_req_{num_requests}.csv'
        call_server(file_name)
        if (num_workers != workers_config[-1]):
            print(f'add {inc_config[i]} workers')
            add_workers(inc_config[i])
        i += 1
        print('------------------')
    throughput_file_name_workers = f'throughput_single_multiple_workers_algo_{current_algo}.csv'
    np.savetxt(throughput_file_name_workers, throughputs , delimiter=',')
    remove_workers(workers_config[-1] - 4) # remove workers to get only 4 (default config)
    print('*******************************************************')
    


# #### Throughput by number of workers

# In[18]:


# throughput_file_name_workers = 'throughput_single_multiple_workers.csv'
# np.savetxt(throughput_file_name_workers, throughputs , delimiter=',')


# In[19]:


# throughputs_workers_from_file = np.genfromtxt(throughput_file_name_workers, delimiter=',')
# workers = [1, 2, 4, 8, 16]
# y_pos = np.arange(len(throughputs_workers_from_file))

# plt.bar(y_pos, throughputs_workers_from_file, align='center', alpha=0.5)
# plt.xticks(y_pos, workers)
# plt.ylabel('Throughput')
# plt.title('Throughput by workers')

# plt.show()


# In[ ]:





# ### Lenskit

# In[41]:


import sys
import math
from binpickle import BinPickleFile
from pathlib import Path

directory_path = 'models'

def exists_model_file(algo):
    full_file_name = Path(directory_path) / algo
    if full_file_name.exists():
        return True
    else:
        return False

def load_for_shared_mem(file_name):
    full_file_name = Path(directory_path) / file_name

    binpickle_file = BinPickleFile(full_file_name, direct=True)
    model = binpickle_file.load()
    return model

def get_predictions_from_model(model, user, items):
    try:
        results = []
        df_preds = model.predict_for_user(user, items)
        for index, value in df_preds.iteritems():
            if not math.isnan(value):
                results.append({'item': index, 'score': value})
        return results
    except:
        print(f"Unexpected preds error for user: {user}, with items: {items}. Error: {sys.exc_info()[0]}")
        raise
        

# Predictions    
async def get_preds_threads_lkpy(num_sem, model, file_name=None, add_throughput=False):
    times = []
    sem = asyncio.Semaphore(num_sem)
    tasks = []    
    num_requests = len(n_rand_users)
    print(f'Number of requests: {num_requests}')
    start_preds = perf_counter()

    async with aiohttp.ClientSession() as session:
        for idx, row in n_rand_users.iterrows():
            task = asyncio.ensure_future(get_user_preds_with_threads_lkpy(row['user'], items, session, sem, times, model))
            tasks.append(task)         

        responses = await asyncio.gather(*tasks)
        time_taken_all = perf_counter() - start_preds
        print_stats(times, time_taken_all, num_requests)
        
        if file_name != None and file_name != '':
            if os.path.exists(file_name):
                os.remove(file_name)
            np.asarray(times)
            np.savetxt(file_name, times, delimiter=',')
        
        if add_throughput:
            throughputs.append(num_requests / time_taken_all)

async def get_user_preds_with_threads_lkpy(user, items, session, sem, times, model):
    async with sem:  # semaphore limits num of simultaneous downloads
        return await get_user_preds_threads_lkpy(user, items, session, times, model)        
        
async def get_user_preds_threads_lkpy(user, items, session, times, model):
    try:
        start = perf_counter()
        results = []
        df_preds = model.predict_for_user(user, items.split(','))
        for index, value in df_preds.iteritems():
            if not math.isnan(value):
                results.append({'item': index, 'score': value})
                
        time_taken = perf_counter() - start
        times.append(time_taken)
        return results
    except:
        print(f"Unexpected preds error for user: {user}, with items: {items}. Error: {sys.exc_info()[0]}")
        raise        


# #### Train models

# In[42]:


import train_save_model
lk_recserver_algos = reader.get_value('lk_recserver_algos')
lk_recserver_algos_not_created = []
for a in lk_recserver_algos:
    if not exists_model_file(f'{a}.bpk'):
        lk_recserver_algos_not_created.append(a)
if len(lk_recserver_algos_not_created) > 0:
    train_save_model.save_models(lk_recserver_algos_not_created)


# In[35]:


for lk_recserver_algo in lk_recserver_algos:
    print(f'Algo: {lk_recserver_algo}')
    print('Lenskit performance:')
    model = load_for_shared_mem(f'{lk_recserver_algo}.bpk')
    file_name = f'lkpy_parallel_threads_8_{lk_recserver_algo}__num_req_{num_requests}.csv'
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_preds_threads_lkpy(8, model, file_name))
    loop.run_until_complete(future)
    #plot_numbers(file_name)
    #hist_numbers(file_name)
    print('------------------')    
    warm_up(lk_recserver_algo, 8, False)
    print('Recommendation server performance:')
    file_name = f'preds_{lk_recserver_algo}_parallel_threads_8_workers_4_num_req_{num_requests}.csv'
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_preds_sem(8, lk_recserver_algo, file_name, True))
    loop.run_until_complete(future)
    #plot_numbers(file_name)
    #hist_numbers(file_name)
    print('*******************************************************')    


# In[ ]:





# In[ ]:




