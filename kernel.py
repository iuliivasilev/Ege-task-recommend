import pandas as pd
import numpy as np

def parse_np_list(x, delim = ' '):
  x = x[1:-1]
  if x.find(delim) == -1:
    if len(x) == 0:
      return np.array([], dtype = int)
    else:
      return np.array([int(x)], dtype = int)
  return np.array(list(map(int,x.split(delim))))

class Task_info:
  def __init__(self, dir_usr, dir_task):
    self.dir_usr = dir_usr
    self.dir_task = dir_task
    self.users = pd.read_excel(dir_usr)
    self.users['rating'] = self.users['rating'].apply(parse_np_list)
    self.users['stories'] = self.users['stories'].apply(parse_np_list)
    self.tasks = pd.read_excel(dir_task)
    self.tasks['degree'] = self.tasks['degree'].apply(parse_np_list)
    self.len_categ = self.tasks['degree'].shape[0]

  def get_task(self, id):
    user_ind = self.users[self.users['id'] == id].index
    rating = self.users.loc[user_ind,'rating'].iloc[0]
    stories = self.users.loc[user_ind,'stories'].iloc[0]
    rec = self.tasks.iloc[self.tasks.apply(lambda x: sum((x['degree'] - np.array(rating))**2),axis = 1).argsort()]
    rec = rec.query("uuid not in @stories")
    #print(rec)
    if rec.shape[0] > 0:
      choose = rec.iloc[0].uuid
    else:
      return None
    self.users.at[user_ind, 'curr_task'] = choose
    return choose
    
  def new_user(self, id):
      if not (id in set(self.users['id'].values)):
        self.users = self.users.append({'id':id,'rating':np.array([0 for i in range(self.len_categ)]), 
                                      'stories':np.array([], dtype = int), 'curr_task':-1
                                      },ignore_index=True)
        print('New user:',id)
      return True
  def get_rating(self, id):
    user_ind = self.users[self.users['id'] == id].index
    return self.users.loc[user_ind,'rating'].iloc[0]
  
  def get_stories(self,id):
    user_ind = self.users[self.users['id'] == id].index
    return self.users.loc[user_ind,'stories'].iloc[0]

  def get_answer(self, id, answer = False):
    user_ind = self.users[self.users['id'] == id].index
    self.uu = user_ind
    uuid = self.users[self.users['id'] == id]['curr_task'].values[0]
    #print(uuid)
    if uuid < 0:
      return None
    task_ind = self.tasks[self.tasks['uuid'] == uuid].index
    rating = self.users.loc[user_ind,'rating'].iloc[0]
    choose = self.tasks.iloc[task_ind,:]
    if answer:
      b = np.clip(choose['degree'].iloc[0] - rating, 0, 3)
      a = self.users.loc[user_ind, 'rating'].iloc[0] + b
      self.users.at[user_ind[0],'rating'] = a
    self.users.at[user_ind[0],'stories'] = np.append(self.users.loc[user_ind,'stories'].iloc[0],choose['uuid'])
    self.users.at[user_ind, 'curr_task'] = -1

  def __del__(self):
    self.users.to_excel(self.dir_usr,  index = False)
    self.tasks.to_excel(self.dir_task, index = False)
