#coding:utf-8
import csv   #csvモジュールをインポートする

#HRS
f = open('../data/572_4_patients_basic_data.csv', 'rb')
dataReader = f.read().split('\r')
print dataReader[1]

#Cirrhous
f1 = open('../data/571_patients_basic_data.csv', 'rb')
dataReader_1 = f1.read().split('\r')

#Output
HRS_out = open('target_hrs.csv', 'w') 
CIR_out = open('target_cir.csv', 'w') 

#CIR
for row_1 in dataReader_1:
   #HRS
   tmp = row_1.split(',')[0]
   i = 0
   for row in dataReader:
       #HRS 
       if tmp == row.split(',')[0]:
           HRS_out.write(tmp)
           HRS_out.write('\n')
           i += 1
           break
       else:
           continue      
   #NOT HRS  
   if i == 0:
       CIR_out.write(tmp)
       CIR_out.write('\n')

HRS_out.close()
CIR_out.close()
