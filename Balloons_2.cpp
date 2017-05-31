
/*
 算法思想：
 1.本算法的主要思想是计算所有情况寻找最优解，假定所有情况是有限的，即圆能放的位置是有限的；
 2.所谓圆能放的位置是有限的是指其圆心x、y坐标的精度只能取到小数点后两位，所以区域内圆心的位置有10000个，通过计算每个位
 置满足条件的最大半径r，从而找出这些点的最大半径；
 3.在寻找最大半径时，每个位置的最大半径的精度只能取到小数点后五位；
 4.满足条件的最大圆将放入一个链表中，这样一来之后的圆在进行位置判断时可以与已放入的圆进行比较，从而判断其是否满足条件；
 */

#include <stdlib.h>
#include <stdio.h>
#include <math.h>

//气球
typedef struct ball
{
    double x;       //圆心x坐标
    double y;		//圆心y坐标
    double r;		//圆半径
}Ball;

//用来储存已经放置的气球
typedef struct ballList
{
    struct ballList * next;
    Ball ball;
}BallList;

void insert(Ball ball);						//插入气球
double distance(Ball b1, Ball b2);          //判断气球之间的距离
double abs(double num);					    //取绝对值
int judge(Ball b);							//判断新加入的气球是否符合规则
void putBall();								//改变气球的初始位置，求的满足条件的气球
void putPoint(double x, double y);			//放置点

BallList *head = NULL;
double step = 0.01;							//改变气球位置的最小单位
int num = 0;                                //放置气球的个数
double sumr = 0;							//用来记录r^2之和

int main()
{
    int n, pointNum, i;
    printf("请输入空间内所要放置的气球数量: ");
    scanf("%d",&n);
    printf("请输入空间内点的数量: ");
    scanf("%d",&pointNum);
    for(i = 0; i < pointNum; i ++)
    {
        printf("请输入第%d个点的坐标(其间用空格隔开)：",i+1);
        double x, y;
        scanf("%lf %lf", &x, &y);
        putPoint(x, y);
    }
    printf("\n球编号\t x坐标\t y坐标\t 半径\t r^2之和\n");
    for(i = 0; i < n; i ++)
    {
        putBall();
    }
    printf("\nr^2之和为:\t %lf\n", sumr);
    return 0;
}

void putPoint(double x, double y)
{
    Ball ball = {x, y, 0};
    insert(ball);
}

void insert(Ball ball)
{
    ballList * newBall = (ballList *)malloc(sizeof(ballList));
    newBall->ball = ball;
    newBall->next = head;
    head = newBall;
}

void putBall()
{
    Ball ball = {-1 + step, -1 + step, 0};
    Ball maxBall = ball;
    int i, j;
    for (i = 0; ball.x < 1; ++i)
    {
        ball.x += step;
        ball.y = -1 + step;
        for (j = 0; ball.y < 1; ++j)
        {
            ball.y += step;
            ball.r = 0;
            double rstep = 0.1;
            while(rstep > 0.00001)
            {
                if(ball.r > maxBall.r)
                {
                    maxBall = ball;
                }
                ball.r += rstep;
                if(!judge(ball))
                {
                    ball.r -= rstep;
                    rstep /= 10;
                }
            }
        }
    }
    if(judge(maxBall))
    {
        insert(maxBall);
        num++;
        sumr += maxBall.r * maxBall.r;
        printf("%d\t %.3lf\t %.3lf\t %.3lf\t %lf \n", num, maxBall.x, maxBall.y, maxBall.r, sumr);
    }
}

int judge(Ball b)
{
    if((abs(b.x) + b.r) > 1 || (abs(b.y) + b.r) > 1)
    {
        return false;
    }
    ballList *tmp = head;
    while(tmp)
    {
        Ball ball = tmp->ball;
        if(distance(b, ball) < b.r + ball.r )
        {
            return false;
        }
        tmp = tmp->next;
    }
    return true;
}

double abs(double num)
{
    if(num > 0)
        return num;
    return 0 - num;
}

double distance(Ball b1, Ball b2)
{
    double x1 = b1.x;
    double y1 = b1.y;
    double x2 = b2.x;
    double y2 = b2.y;
    return pow((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2), 0.5);
}
