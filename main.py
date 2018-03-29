# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 10:54:48 2018

@author: chengch
"""

from PIL import Image
import numpy as np

codeLib = '@# %'#生成字符画所需的字符集
count = len(codeLib) # 选用字符得个数

k = 2 # 这个值取决于坐标轴所占得字符数，如果两个坐标轴都是单轴得话，可以是2，但是如果都是双轴得话就得是4.也可以通过图片尺寸变换，把坐标变得分辨率降低，然后就是单轴了

fp = open("F:\\2.jpg",'rb') #打开源图文件
image_file = Image.open(fp)
image_file=image_file.resize((int(image_file.size[0]), int(image_file.size[1]*0.6)))#调整图片大小
image_file = image_file.convert("L")#灰度化

def transform1(image_file):
  #  image_file = image_file.convert("L")#转换为黑白图片，参数"L"表示黑白模式
    codePic = ''
    for w in range(0,image_file.size[1]):  #size属性表示图片的分辨率，'0'为横向大小，'1'为纵向
        for h in range(0,image_file.size[0]):
            gray = image_file.getpixel((h,w)) #返回指定位置的像素，如果所打开的图像是多层次的图片，那这个方法就返回一个元组
            codePic = codePic + codeLib[int(((count-1)*gray)/256)]#建立灰度与字符集的映射
        codePic = codePic+'\n'
    return codePic

tmp = open('F:\\yuan.txt','w')
tmp.write(transform1(image_file))
tmp.close() #写入源图片转换后得文本
#
arr = np.array(image_file)
lin = arr.sum(axis=0) # 列相加
row = arr.sum(axis=1) # 行相加
### 根据灰度值得大小来确定得，有写东西得地方，值就很小。然后根据行和列相加和来判断是没有写东西得地方，还是坐标轴。
ind_lin = []
ind_row = []
#
for i in np.arange(k):
    l_ind = np.argmin(lin)
    ind_lin.append(l_ind)
    lin[l_ind] += 100000
    
    r_ind = np.argmin(row)
    ind_row.append(r_ind)
    row[r_ind] += 100000
#    
ind_lin = sorted(ind_lin)
ind_row = sorted(ind_row)
#
smart_arr = arr[ind_row[0]+1:ind_row[1]][:,ind_lin[0]+1:ind_lin[1]]#进行图片裁切

#对裁切后得矩阵进行180度旋转

re_smart_arr = smart_arr[::-1][:,::-1]

img = Image.fromarray(re_smart_arr) #坐标轴之内得图
#
tmp = open('F:\\hou.txt','w')
tmp.write(transform1(img))
tmp.close()#保存修改后得图片

result = []

for l in np.arange(len(re_smart_arr[1])):
    result.append(np.argmin(re_smart_arr[:,l]))    
    
result = np.array(result)
result.dtype = 'int32'
result = result[::8]
result = result[::-1]

plt.plot(np.arange(len(result)),result)
plt.savefig('F://test.png',dpi=200)
plt.show()