# -*- coding:utf-8 -*-
import pandas as pd

jobs = pd.read_csv('jobs.csv')
stus = pd.read_csv('stu.csv')
classes = pd.read_csv('class.csv')

# 1. SELECT * FROM data;
print(jobs)

# 2. SELECT * FROM data LIMIT 10;
print(jobs.head(10))

# 3. SELECT id FROM data;  //id 是 data 表的特定一列
print(jobs['id'])
#
# 4. SELECT COUNT(id) FROM data;
print(jobs['id'].size)

# 5. SELECT * FROM data WHERE id<1000 AND age>30;
print(jobs[(jobs['id'] > 1000) & (jobs['city'] == '北京')])

# 6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
print (jobs.groupby('city').aggregate({'positionId': 'count', }))

# 7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
print(pd.merge(stus, classes, how='inner', on='id'))

# 8. SELECT * FROM table1 UNION SELECT * FROM table2;
print(pd.concat([stus, classes], axis=0, ignore_index=True))

# 9. DELETE FROM table1 WHERE id=10;
print(stus.drop(stus[stus['id']==10].index, axis=0))

# 10. ALTER TABLE table1 DROP COLUMN column_name
print(stus.drop(['性别'], axis=1))
