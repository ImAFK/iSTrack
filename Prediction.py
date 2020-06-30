
# coding: utf-8

# In[1]:


get_ipython().system('pip install numpy')
get_ipython().system('pip install h5py')
get_ipython().system('pip install pandas')
get_ipython().system('pip install afs2-datasource')
get_ipython().system('pip install nest_asyncio')
get_ipython().system('pip install networkx')
get_ipython().system('pip install python-louvain')

#from community import community_louvain
import nest_asyncio
import networkx as nx
import pandas as pd
import numpy as np
from afs2datasource import DBManager, constant
import os

nest_asyncio.apply()

config = {}
envs = {
    "parameter": 20
}

for env, default in envs.items():
    config.update({
        env: os.getenv(env, default)
    })


# In[2]:


def push2DB(collection, edge, records):
    manager.create_table(table_name = collection)
    if not edge:
        # output prediction
        columns = ['name', 'latitude','longitude', 'value']
        
    else:
        # init Edge knowledge
        columns = ['commu', 'sarea', 'sna', 'address', 'lng', 'lat']
        records = records
    
    manager.insert(table_name = collection, columns = columns, records = records)


# In[3]:


# Source DB for Edge knowledge
df_edge = pd.DataFrame([
    ['2020-01-03 16:00:00', '捷運松山站(3號出口)', '2020-01-03 17:00:00', '捷運市政府站(3號出口)', '0:13:34' ,'2020-01-03'], 
    ['2020-01-03 15:00:00', '大稻埕公園', '2020-01-03 16:00:00', '永樂市場', '0:33:00', '2020-01-03'],
    ['2020-01-03 14:00:00', '捷運台電大樓站(2號出口)', '2020-01-03 14:00:00', '捷運公館站(2號出口)', '0:10:59', '2020-01-03'],
    ['2020-01-03 23:00:00', '錦州吉林路口', '2020-01-03 23:00:00', '捷運士林站(2號出口)', '0:26:04', '2020-01-03'],
    ['2020-01-03 17:00:00', '捷運忠孝新生站(2號出口)', '2020-01-03 17:00:00', '捷運忠孝新生站(2號出口)', '0:13:10', '2020-01-03'],
    ['2020-01-03 17:00:00', '中山青島路口', '2020-01-03 17:00:00', '蔣渭水紀念公園', '0:22:11', '2020-01-03'],
    ['2020-01-03 07:00:00', '捷運北投站', '2020-01-03 07:00:00', '捷運北投站', '0:22:19', '2020-01-03'],
    ['2020-01-03 17:00:00', '錦德公園', '2020-01-03 17:00:00', '萬華車站', '0:10:59', '2020-01-03'],
    ['2020-01-03 07:00:00', '牯嶺公園', '2020-01-03 08:00:00', '羅斯福寧波東街口', '0:07:03', '2020-01-03'],
    ['2020-01-03 21:00:00', '林森公園', '2020-01-03 21:00:00', '民族玉門街口', '0:18:12', '2020-01-03'],
    ['2020-01-03 06:00:00', '北投運動中心', '2020-01-03 06:00:00', '捷運石牌站(2號出口)', '0:04:06', '2020-01-03'],
    ['2020-01-03 18:00:00', '台灣科技大學', '2020-01-03 18:00:00', '捷運公館站(2號出口)', '0:03:33', '2020-01-03'],
    ['2020-01-03 14:00:00', '捷運石牌站(2號出口)', '2020-01-03 14:00:00', '捷運石牌站(2號出口)', '0:08:37', '2020-01-03']
])

df_loc = pd.DataFrame([
    ['中正區', '華山文創園區', '忠孝東路二段41號前', 50,121.5284882,25.04366875],
    ['南港區', '捷運昆陽站(1號出口)','捷運昆陽站1號出口外停車場旁', 42,121.5923767,25.05014229],
    ['南港區', '捷運南港展覽館站(5號出口)', '研究院路/市民大道(東北側)',26,121.6166916,25.05468941],
    ['信義區', '五常公園', '松隆路/虎林街30巷口(西南側)', 36,121.5746689,25.04813957],
    ['大安區', '金山愛國路口','愛國東路/金山南路(西南側)',54,121.5265503,25.0316391],
    ['大安區', '基隆長興路口','基隆路/長興街(東南側)',40,121.5443497,25.0170536],
    ['大安區', '辛亥新生路口', '辛亥路/新生南路(高架橋下)',30,121.5345612,25.02241325]]
)


# In[4]:


def do_predict():
    pass


# In[6]:


manager = DBManager( db_type = constant.DB_TYPE['MONGODB'],
                    username = "5bdc632c-f0db-4775-aec5-1ab414d25ab0",
                    password = "uHC14kaunATUPRHjGmuVmxHs",
                    host = "13.76.163.151",
                    port = 27017,
                    database = "db2e5816-4a9e-4d99-8194-cc688e92d8f9",
                    collection = "test234",
                    querySql = "{}" )

# Connect DB
manager = DBManager()
manager.connect()

in_collection = 'record'
edge_collection = 'connection_between_place'
out_collection = 'pred_value_of_node'

# in first time, we built a prediction while the collection input is not exist, add it
if not manager.is_table_exist(in_collection):
    manager.create_table(table_name = in_collection)
    
    
# make a prediction with the input data
else:
    # 1. the input data as the weight on node
    # 2. the prior knowledge about edge would be kind of connection strength,
    #    and we would predict the new weight and to give some advice based on it.
    
    #  grab the data restore it in df type
    df_new_info = manager.execute_query()


    
    if not manager.is_table_exist(edge_collection):
    # first time to predict init edge info
        '''Graph = nx.Graph()
    
        for i in range(df_edge.shape[0]):
            Graph.add_edge(df_edge.iloc[i][1], df_edge.iloc[i][3])
    
        partition = community_louvain.best_partition(Graph, resolution=0.63)
        commun = {}
        for station, commu in partition.items():
            if commu not in commun.keys():
                commun.update({commu:[station]})
            else:
                commun[commu].append(station)

        station_info = []
        for each in df_loc.iterrows():
            try:
                station_info.append([partition[each[1][1]], each[1][0], each[1][1], each[1][2], each[1][4], each[1][5]])
            except:
                station_info.append([-1, each[1][0], each[1][1], each[1][2], each[1][4], each[1][5]])'''
        push2DB(edge_collection, True, station_info)
        
    if manager.is_table_exist(out_collection):
        manager.delete_table(table_name = out_collection)
        records = do_predict()
        
        records = [
            ['NTUST', 25.010811, 121.539797, 0.9],
            ['NTU', 25.015192, 121.537826, 0.95],
            ['MRT GongGuan', 25.014767, 121.534235, 0.98]
        ]
        push2DB(out_collection, False, records)

