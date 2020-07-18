学习笔记
# Pandas 相关操作
1.导入数据

    pd.read_csv(filename_path)：从CSV文件导入数据
    pd.read_table(filename_path)：从限定分隔符的文本文件导入数据
    pd.read_excel(filename_path)：从Excel文件导入数据
    pd.read_sql(query, connection_object)：从SQL表/库导入数据
    pd.read_json(json_string)：从JSON格式的字符串导入数据
    pd.read_html(url)：解析URL、字符串或者HTML文件，抽取其中的tables表格
    pd.read_clipboard()：从你的粘贴板获取内容，并传给read_table()
    pd.DataFrame(dict)：从字典对象导入数据，Key是列名，Value是数据

2.导出数据

    df.to_csv(filename_path)：导出数据到CSV文件
    df.to_excel(filename_path)：导出数据到Excel文件
    df.to_sql(table_name, connection_object)：导出数据到SQL表
    df.to_json(filename_path)：以Json格式导出数据到文本文件

3.创建测试数据

    pd.DataFrame(np.random.rand(20,5))：创建20行5列的随机数组成的DataFrame对象
    pd.Series(my_list)：从可迭代对象my_list创建一个Series对象
    df.index = pd.date_range('1900/1/30', periods=df.shape[0])：增加一个日期索引

4.查看、检查数据

    df.head(n)：查看DataFrame对象的前n行（不加参数，默认前10行）
    df.tail(n)：查看DataFrame对象的最后n行（不加参数，默认后10行）
    df.shape()：查看行数和列数（维度查看）
    df.info()：查看索引、数据类型和内存信息
    df.describe()：查看数值型列的汇总统计
    s.value_counts(dropna=False)：查看Series对象的唯一值和计数
    df.apply(pd.Series.value_counts)：查看DataFrame对象中每一列的唯一值和计数
    df.dtypes：查看每一列的数据类型（扩展：df['two'].dtypes，查看“two”列的类型）
    df.isnull()：查看空置(注：空置部分会用true显示，不是空置False显示)（扩展：df['two'].isnull，查看“two”这一列的空置）
    df.values：查看数据表的值
    df.columns：查看列名称

5.数据选取

    df.isin([5])：判断全部数据值中是否有5
    df[col].isin([5])：判断列col中是否有5
    df[col]：根据列名，并以Series的形式返回列
    df[[col1, col2]]：以DataFrame形式返回多列
    s.iloc[0]：按位置选取行数据
    s.loc['index_one']：按索引选取行数据
    df.loc[:,'reviews']      获取指定列的数据 注意： 第一个参数为：表示所有行，第2个参数为列名，设置获取列名为review的数据
    df.loc[[0,2],['customername','reviews','review_fenci']]   选择指定的多行多列 参数说明： [0,2] 这个列表有两个元素0,2表示选择第0行和第2行['customername','reviews','review_fenci']这个列表有3个元素表示选择列名为'customername','reviews','review_fenci‘的这3列
    df.iloc[0,:]：返回第一行
    df.iloc[0,0]：返回第一行的第一个元素
    df.ix[0] 或 df.ix[raw] ：ix函数可以根据行位置或行标签选择行数据

 注：loc函数根据行/列标签(用户自定义的行名、列名)进行行选择；

         iloc函数根据行/列位置(默认的行列索引)进行行选择；

6.数据清理

    df.columns = ['a','b','c']：重命名列名
    pd.isnull()：检查DataFrame对象中的空值，并返回一个Boolean数组
    pd.notnull()：检查DataFrame对象中的非空值，并返回一个Boolean数组
    df.dropna()：删除所有包含空值的行
    df.dropna(axis=1)：删除所有包含空值的列
    df.dropna(axis=1,thresh=n)：删除所有小于n个非空值的行
    df.fillna(x)：用x替换DataFrame对象中所有的空值（注：fillna()会填充nan数据，返回填充后的结果。如果希望在原DataFrame中修改，则把inplace设置为True。如，df.fillna(0,inplace=True)）
    mydf['列名']=mydf['列名'].fillna(0)   某一列的空值补零
    s.astype(float)：将Series中的数据类型更改为float类型
    df[col].astype(float)：将DataFrame某列数据类型改为float类型
    s.replace(1,'first')：用‘first’代替所有等于1的值（替换的是值，不是列名也不是索引名）
    s.replace([1,3],['one','three'])：用'one'代替1，用'three'代替3
    df[col].replace(1,1.0,inplace=True)：列col中的值1用1.0替换
    df.replace([1,3],['one','three'])
    df.rename(columns=lambda x: x + 1)：批量更改列名
    df.rename(columns={'old_name': 'new_ name'})：选择性更改列名
    df.set_index('column_one')：将column_one这一列变为索引列
    df.rename(index=lambda x: x + 1)：批量重命名索引
    df[col]=df[col].str.upper()或df[col].str.lower()：基于列的大小写转换
    df[col]=df[col].map(str.strip)：清除某列的空格
    df.drop_duplicates(subset=col,keep='fisrt',inplace=Flase)：删除重复值

注：这个drop_duplicate方法是对DataFrame格式的数据，去除特定列下面的重复行。返回DataFrame格式的数据。

    subset : column label or sequence of labels, optional      用来指定特定的列，默认所有列
    keep : {‘first’, ‘last’, False}, default ‘first’      删除重复项并保留第一次出现的项
    inplace : boolean, default False        是直接在原来数据上修改还是保留一个副本

7.数据处理

    df[df[col] > 0.5]：选择col列的值大于0.5的行
    df.sort_values(col1)：按照列col1排序数据，默认升序排列
    df.sort_values(col2, ascending=False)：按照列col1降序排列数据
    df.sort_values([col1,col2], ascending=[True,False])：先按列col1升序排列，后按col2降序排列数据
    df.groupby(col)：返回一个按列col进行分组的Groupby对象
    df.groupby([col1,col2])：返回一个按多列进行分组的Groupby对象
    df.groupby(col1)[col2]：返回按列col1进行分组后，列col2的均值
    df.pivot_table(index=col1, values=[col2,col3], aggfunc=max)：创建一个按列col1进行分组，并计算col2和col3的最大值的数据透视表
    df.groupby(col1).agg(np.mean)：返回按列col1分组的所有列的均值
    data.apply(np.mean)：对DataFrame中的每一列应用函数np.mean
    data.apply(np.max,axis=1)：对DataFrame中的每一行应用函数np.max
    df.isin

8.数据合并

    df1.append(df2)：将df2中的行添加到df1的尾部
    df.concat([df1, df2],axis=1)：将df2中的列添加到df1的尾部
    df1.join(df2,on=col1,how='inner')：对df1的列和df2的列执行SQL形式的join

9.数据统计

    df.describe()：查看数据值列的汇总统计
    df.mean()：返回所有列的均值
    df.corr()：返回列与列之间的相关系数
    df.count()：返回每一列中的非空值(NaN)的个数
    df.max()：返回每一列的最大值
    df.min()：返回每一列的最小值
    df.median()：返回每一列的中位数
    df.std()：返回每一列的标准差
    df.sum()：返回所有行的和





# jieba 中文分词
		cut_all 是否为全模式
    jieba.cut(string, cut_all=False)  
    jieba.cut(string, cut_all=True)
    jieba.cut(string, HMM=False)
    jieba.cut_for_search(string)

    添加黑名单

    stop_words = r'stop_words.txt'  # 一行一个单词
    jieba.analyse.set_stop_words(stop_words)
    textrank = jieba.analyse.textrank(text, topK=5, withWeight=False)
    pprint.pprint(textrank)

    自定义词库

    user_dict = r'user_dict.txt'
    jieba.load_userdict(user_dict)
    result = jieba.cut(string, cut_all=False)

    分词和合词

    jieba.suggest_freq('中出', True)       # 合词
    jieba.suggest_freq(('中','将'), True)  # 分词

# snownlp 情感分析

    常用操作
    s = SnowNLP(text) 	文本分析 	
    s.words 	中文分词 	
    list(s.tags) 	词性标注 	隐马尔可夫模型
    s.sentiments 	情感分析 	0 ~ 1，朴素贝叶斯分类器
    s.pinyin 	转拼音 	Trie 叔
    s.han 	繁体简化 	
    s.keywords(limit=5) 	关键字提取 	
    s.tf 	词频 	
    s.idf 	词条信息量 	

    模型训练：

    from snownlp import seg
    seg.train('train.txt')
    seg.save('seg.marshal')
    # 修改 snownlp/seg/__init__py 的 data_path 指向新的模型即可

