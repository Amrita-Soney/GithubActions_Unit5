# -*- coding: utf-8 -*-
"""spark.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pvlMW62dx7sLoMRXGyVxDNYGl_hM-nB9

Khushi Sinha - 2021UCA1872

Esha Garg - 2021UCA1821

Amrita Soney - 2021UCA1831
"""

pip install findspark

pip install pyspark

import findspark
findspark.init()
import pyspark
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
from pyspark.sql.functions import *

path = ['/content/Ecommerce_Customers.csv']
dataset = spark.read.options(inferSchema= True, header = True).csv(path)

dataset.printSchema()

dataset.show(5)

dataset.count()

dataset.limit(5).toPandas()

dataset.orderBy('Yearly Amount Spent', ascending = False).limit(5).toPandas()



"""LINEAR REGRESSION

"""

from pyspark.ml.regression import LinearRegression

from pyspark.ml.linalg import Vectors

from pyspark.ml.feature import VectorAssembler

fa = VectorAssembler(inputCols=["Time on App", "Time on Website", "Length of Membership"], outputCol="Independent Features")

output = fa.transform(dataset)

output.toPandas()

output.select("Independent Features").show()

output.columns

finalised_data = output.select("Independent Features", "Yearly Amount Spent")
finalised_data.toPandas()

train_data, test_data = finalised_data.randomSplit ([0.80,0.20])
regressor = LinearRegression(featuresCol='Independent Features', labelCol='Yearly Amount Spent')
regressor=regressor.fit(train_data)

regressor.coefficients

regressor. intercept

pred_results=regressor.evaluate(test_data)
pred_results.predictions.show(40)



"""PERFORMANCE ANALYSIS"""

trainingSummary = regressor.summary
print ("Root Mean Squared Error on training data: %f" % trainingSummary.rootMeanSquaredError)
print("R Squared (R) on training data: %f" % trainingSummary.r2)

train_data.describe() . show ()

lr_predictions = regressor. transform(test_data)
lr_predictions.select ("prediction", "Yearly Amount Spent", "Independent features"). show(5)
from pyspark.ml.evaluation import RegressionEvaluator
lr_evaluator = RegressionEvaluator(predictionCol = "prediction", labelCol="Yearly Amount Spent", metricName = "r2")
r2_test = lr_evaluator.evaluate(lr_predictions)
print("R Squared (R2) on test data= %g" % r2_test)

dataset.show(5,False)

"""RDD"""

rddL = spark.sparkContext.textFile('/content/Ecommerce_Customers.csv')
rddL.first()

rddL_header = rddL.first ()

rddL_remain = rddL.filter (lambda line: line!=rddL_header)
print(rddL_remain.first())

rddL_remain.map(lambda line: line.split(";")).count ()

rddL2 = rddL.map(lambda line: (line.split(",")[-1],
  line.split(",")[0]) )
rddL2.countByKey()

rddL.filter(lambda x : "C").collect()