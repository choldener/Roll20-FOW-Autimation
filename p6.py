sum_num = 0
sum_square = 0
for i in range(1,101):
    print(i)
    sum_num = i**2 + sum_num
    sum_square = i + sum_square

sum_square = sum_square **2 
print("sum_num:" + str(sum_num))
print("sum_square:" + str(sum_square))
dif = sum_square - sum_num
print(dif) #25164150
