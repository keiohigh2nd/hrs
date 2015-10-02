#coding:utf-8
import csv   #csvモジュールをインポートする

#HRS
f = open('../input_data/target_all.csv', 'rb')
dataReader = f.read().split('\n')


#Output
align_out = open('../input_data/align_target_hrs.csv', 'w') 

#CIR

k = 0
total = 0
under = 0
for i in xrange(len(dataReader)):
       k += 1

       tmp = dataReader[i].split(',')[0]
       tmp_p = dataReader[i-1].split(',')[0]
       tmp_m = dataReader[i+1].split(',')[0]
       #STOP SIGN
       if tmp == tmp_m and tmp != tmp_p:
         total += dataReader[i].split(',')[9]
         under += 1
         ave = float(total)/under
         under, total = 0, 0 
         align_out.write(dataReader[i])   
         align_out.write(',%s' % ave)   
         align_out.write('\n')   
       #Continue
       if tmp == tmp_p and tmp == tmp_m:
         total += dataReader[i].split(',')[9]
         under += 1
         continue

       if k > 10:
         break



align_out.close()
