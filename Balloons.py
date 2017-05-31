# coding=utf-8

import random

#     FileName: Balloons.py
#         Desc: Put balloons into a box.
#       Author: HusterHope
#        Email: luhp9696@gmail.com
#    Reference: https://github.com/DongZhuoran
#      Version: 0.0.1
#   LastChange: 2016-05-25 17:02:23

INF = 1e9
T = 100               #初始温度
delta = 0.9         #温度下降速度
THRESHOLD = 1e-6   #停止搜索阈值条件
MOVE = 100         #确定每个圆圆心的比较次数
PREOPT = 1e-6      #最小圆半径精度
alpha = 0.2        #学习速率
MINEX = 1e-1       #有解条件

dx = [ 0, 0, -1, 1 ]
dy = [ 1, -1, 0, 0 ]  #上下左右四个方向


class Circle:
    def __init__(self):
        self.radius = 0
        self.x = 0
        self.y = 0


def initialize(n):
    cir = [Circle()]*n
    for i in range(n):
        cir[i].radius = 0
        cir[i].x = 0
        cir[i].y = 0
    return cir

def dist(A,B):#A，B圆心的距离
    return ((A.x - B.x)**2+(A.y - B.y)**2)**(1/2)

def Getsum(cir,n,c):
    ans = 0
    for i in range(n):
        ans += (cir[i].radius + c.radius - dist(cir[i], c))**2
    if (c.x + c.radius > 1):
        ans += (c.x + c.radius - 1)**2
    if (c.x - c.radius < -1):
        ans += (c.x - c.radius + 1)**2
    if (c.y + c.radius > 1):
        ans += (c.y + c.radius - 1)**2
    if (c.y - c.radius < -1):
        ans += (c.y - c.radius + 1)**2
    return ans

def GetCenter(cir,n):
    c=Circle()
    flag = 0
    c.radius = 0
    #圆心（x,y）在－1，1的范围内，我们随机试探
    c.x = 2 * random.random() - 1
    c.y = 2 * random.random() - 1
    while (flag < n):
        c.x = 2 * random.random() - 1
        c.y = 2 * random.random() - 1
        flag = 0
        for i in range(n):  #问题： for (int i = 0, flag = 0; i < n; i++){flag++;}最后flag=?
            if (dist(cir[i], c) > cir[i].radius):
                flag+=1
            else:
                break
    return c

def GetCircle(cir,n,curradius):
    MinCir=Circle()
    MinEx = INF
    MinCir.radius = 0
    MinCir.x = 0
    MinCir.y = 0
    #配合梯度下降法使用
    k=0
    while (k < MOVE):
        c = GetCenter(cir, n)
        c.radius = curradius
        Ex = Getsum(cir, n, c)
        if (Ex < MinEx):
            MinCir = c
            MinEx = Ex
        k+=1
    return MinCir

def optimize(cir,n):
    x1 = cir[n - 1].x
    y1 = cir[n - 1].y
    ax = 0
    ay = 0
    for i in range(n):
        j=i+1
        while(j < n):
            ax -= 2 * (cir[i].radius + cir[j].radius - dist(cir[i], cir[j])**0.5) * dist(cir[i], cir[j])**(-0.5) * (x1 - cir[j].x)
            ay -= 2 * (cir[i].radius + cir[j].radius - dist(cir[i], cir[j])**0.5) * dist(cir[i], cir[j])**(-0.5) * (y1 - cir[j].y)
            j+=1
        if (cir[i].x + cir[i].radius > 1):
            ax += 2 * (cir[i].x + cir[i].radius - 1)
        if (cir[i].x - cir[i].radius < -1):
            ax += 2 * (cir[i].x - cir[i].radius + 1)
        if (cir[i].y + cir[i].radius > 1):
            ay += 2 * (cir[i].y + cir[i].radius - 1)
        if (cir[i].y - cir[i].radius < -1):
            ay += 2 * (cir[i].y - cir[i].radius + 1)
    x2 = x1 - alpha * ax
    y2 = y1 - alpha * ay
    cir[n - 1].x = x2
    cir[n - 1].y = y2
    #while ((x2 - x1 > PREOPT) && (y2 - y1) > PREOPT)
    '''
    while (ax <= 0 and ay == 0):
        x1 = x2
        y1 = y2
        i = 0
        while(i < n):
            j=i+1
            while(j < n):
                ax -= 2 * (cir[i].radius + cir[j].radius - dist(cir[i], cir[j])**0.5) * dist(cir[i], cir[j])**(-0.5) * (x1 - cir[j].x)
                ay -= 2 * (cir[i].radius + cir[j].radius - dist(cir[i], cir[j])**0.5) * dist(cir[i], cir[j])**(-0.5) * (y1 - cir[j].y)
                j+=1
            if (cir[i].x + cir[i].radius > 1):
                ax += 2 * (cir[i].x + cir[i].radius - 1)
            if (cir[i].x - cir[i].radius < -1):
                ax += 2 * (cir[i].x - cir[i].radius + 1)
            if (cir[i].y + cir[i].radius > 1):
                ay += 2 * (cir[i].y + cir[i].radius - 1)
            if (cir[i].y - cir[i].radius < -1):
                ay += 2 * (cir[i].y - cir[i].radius + 1)
            i+=1
        x2 = x1 - alpha * ax
        y2 = y1 - alpha * ay
        cir[n - 1].x = x2
        cir[n - 1].y = y2
    '''
    #/*printf("delta1 = %f, delta2 = %f\n", x2 - x1, y2 - y1);
    #getchar();*/
    return cir[n - 1]

def Search(cir,n):
    ans=0
    t = T
    flag = [0] * n
    while (t > THRESHOLD):
        for i in range(n):
            curradius = PREOPT#最小半径
            if (flag[i] == 1):
                continue
            c = GetCircle(cir,i, curradius)#第i 个圆
            #梯度下降法优化实现
            cir[i] = c
            c = optimize(cir, i + 1)
            while (Getsum(cir, i, c) < MINEX / n):
                #print "curradius = ",curradius
                curradius *= 1.1
                c = GetCircle(cir, i, curradius)
                cir[i] = c
                c = optimize(cir, i + 1)
                if (Getsum(cir, i, c) > MINEX / n):
                    k=0
                    while (k < 10 and Getsum(cir, i, c) > MINEX / n):
                        c = GetCircle(cir, i, curradius)
                        cir[i] = c
                        c = optimize(cir, i + 1)
                        k+=1
            c.radius = curradius / 1.21
            cir[i] = c
            flag[i] = 1
            ans += Getsum(cir, i, c)
        if (ans < MINEX):
            return ans
        else:
            t = t*delta
    return ans

def main():
    while (1):
        #input
        print "Please enter the number of circles:"
        num = input()
        if (num > 0):
            #Initialize circles
            cir = initialize(num)
            #find the position and radius
            ans = Search(cir, num)
            if (ans == -1):
                print "There is no answer, please try again"
            else:
                for i in range(num):#output for each
                    print "The radius and coordinate are:",cir[i].radius , cir[i].x , cir[i].y
                #total area
                #print ans
        else:
            break

main()