# -*- coding: utf-8 -*-
from pyspark.ml.base import Transformer
from pyspark.ml.classification import NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import Tokenizer, IDF, HashingTF, StringIndexer
from pyspark.sql import SparkSession
import jieba
from pyspark.sql.functions import *
from pyspark.sql.types import *
# python3.6使用下面的方式进行加载
import importlib
import sys

importlib.reload(sys)
# python3.6不再有下面的方法
# sys.setdefaultencoding('utf8')
# 创建sparksession
spark = SparkSession.builder.appName("PySpark NB Test").enableHiveSupport().getOrCreate()
# 读取hive数据
df = spark.sql("select sentenceabel from badou.news_noseg")
df.show()


# 定义,l结巴切词方法
def seg(text):
    return ''.join(jieba.cut(text, cut_all=True))


seg_udf = udf(seg, StringType())

# 对数据进行结巴切词
df_seg = df.withColumn('seg', seg_udf(df.sentence)).select('seg', 'label')
df_seg.show()
# 将分词做成ArrayType()
tokenizer = Tokenizer(inputCol='seg', outputCol='words')
assert isinstance(tokenizer,Transformer)
df_seg_arr = tokenizer.transform(df_seg).select('words', 'label')
df_seg_arr.show()

# 切词后的文本特征处理
tf = HashingTF(numFeatures=1 << 18, binary=False, inputCol='words', outputCol='rawfeatures')
assert isinstance(tf,Transformer)
df_tf = tf.transform(df_seg_arr).select('rawfeatures', 'label')
df_tf.show()

idf = IDF(inputCol='rawfeatures', outputCol='features')
idfModel = idf.fit(df_tf)
assert isinstance(idfModel,Transformer)
df_tf_idf = idfModel.transform(df_tf)
df_tf_idf.show()

# label数据处理
stringIndexer = StringIndexer(inputCol='label', outputCol='indexed', handleInvalid='error')
indexer = stringIndexer.fit(df_tf_idf)
assert isinstance(indexer,Transformer)
df_tf_idf_lab = indexer.transform(df_tf_idf).select('features', 'indexed')

df_tf_idf_lab.show()

# 切分训练集和预测集
splits = df_tf_idf_lab.randomSplit([0.7, 0.3], 123)
train = splits[0]
test = splits[1]

# 定义模型
nb = NaiveBayes(featuresCol='features', labelCol='indexed', predictionCol='prediction',
                probabilityCol='probability', rawPredictionCol='rawPrediction',
                smoothing=1.0, modelType='multinomial')
# 模型训练
model = nb.fit(train)
assert isinstance(model,Transformer)
# 预测集训练
predictions = model.transform(test)
predictions.show()

# 计算准确率
evaluator = MulticlassClassificationEvaluator(labelCol='indexed',
                                              predictionCol='prediction',
                                              metricName='accuracy')
accuracy = evaluator.evaluate(predictions)
print("Test set accuracy =" + str(accuracy))
