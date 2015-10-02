#coding:utf-8
import csv   #csvモジュールをインポートする

#HRS
f = open('../data/571_blood_preassure.csv', 'rb')
dataReader = f.read().split('\r')
print dataReader[1]

#Cirrhous
f1 = open('../input_data/only_cre_basic_data.csv', 'rb')
dataReader_1 = f1.read().split('\r')

#Output
HRS_out = open('../input_data/bp_cre_basic_data.csv', 'w') 

#CIR
for row_1 in dataReader_1:
   #HRS
   tmp = row_1.split(',')[0]
   i = 0
   for row in dataReader:
       #HRS 
       if tmp == row.split(',')[0]:
           HRS_out.write(row_1)
           HRS_out.write(',')
           HRS_out.write(row.split(',')[4])
           HRS_out.write('\n')
           i += 1
           break
       else:
           continue      
   #NOT HRS  
   if i == 0:
       HRS_out.write(row_1)
       HRS_out.write(',')
       HRS_out.write('0')
       HRS_out.write('\n')

HRS_out.close()
