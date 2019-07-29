import random,itertools,pygame,sys
pygame.init()
screencaption=pygame.display.set_caption('2048小游戏')
screen=pygame.display.set_mode([1320,900])
screen.fill([230,230,230])

class Gamefield:
    def __init__(self,win_value=2048):
        self.win_value = win_value
        self.best_score1 = 0
        self.score1 = 0
        self.best_score2 = 0
        self.score2 = 0

    #画图形界面（此函数值负责构建图形界面窗口，没有将值绘画在界面上）
    def init_screen(self):
        screen.fill([230, 230, 230])
        for i in range(4):
            for j in range(8):
                left = 150 * j + 10 * j + 15
                top = 150 * i + 10 * i + 110
                if j > 3:
                    left += 20
                pygame.draw.rect(screen, [120, 120, 120], [left, top, 150, 150], 0) #画长宽都是150的方块
        self.draw_number('历史最高：'+str(self.best_score1),330,25,30,(0,120,120))
        self.draw_number('当前分数：' + str(self.score1), 330, 60, 30, (0, 120, 120))
        self.draw_number('历史最高：' + str(self.best_score2), 990, 25, 30, (0, 120, 120))
        self.draw_number('当前分数：' + str(self.score2), 990, 60, 30, (0, 120, 120))
        game.draw_number('移动：上(w) 下(s) 左(a) 右(d) 重置(r)', 330, 780, 30, (0, 0, 0))
        game.draw_number('移动：上(↑) 下(↓) 左(←) 右(→) 重置(r)', 990, 780, 30, (0, 0, 0))
        pygame.draw.line(screen, (120,120,120), [0, 100], [1320, 100], 5)
        pygame.draw.line(screen, (120, 120, 120), [0, 750], [1320, 750], 5)
        pygame.draw.line(screen, (120, 120, 120), [2.5, 100], [2.5, 750], 5)
        pygame.draw.line(screen, (120, 120, 120), [660, 100], [660, 750], 5)
        pygame.draw.line(screen, (120, 120, 120), [1317.5, 100], [1317.5, 750], 5)

    #把字符数字画到界面对应位置
    def draw_number(self,str,left,top,font=60,color=(0, 0, 128)):
        # 创建一个Font对象
        fontObj = pygame.font.SysFont('arplukaitwmbe', font)

        # fontObj.render(字符串,True或False(指定是否要抗锯齿),字体颜色，[背景底色])的返回一个Surface对象
        textSurfaceObj = fontObj.render(str, True, color)

        # Surface对象的get_rect()方法，从Surface对象创建一个Rect对象,这个Rect对象可以计算出文本的正确坐标
        textRectObj = textSurfaceObj.get_rect()

        # 将Rect对象的中心设置为(left,top)
        textRectObj.center = (left,top)

        # 在屏幕绘制文本
        screen.blit(textSurfaceObj, textRectObj)

    #每次移动后，重画界面
    def init_ui(self,flag,li1,li2):
        self.init_screen()  #调用函数画图形界面
        if flag == 1:
            if ' ' in list(itertools.chain(*game_list1)):    #flag = 1表示第一个列表移动，如果列表还有空位置，则新产生一个数，没有则不产生
                self.create_num1()
        if flag == 2:
            if ' ' in list(itertools.chain(*game_list2)):    #flag = 2表示第二个列表移动，如果列表还有空位置，则新产生一个数，没有则不产生
                self.create_num2()
            # 把列表里的数值画进图形界面里
        for i in range(4):
            for j in range(4):
                left = 90 + 160 * j
                top = 195 + 160 * i
                self.draw_number(str(li1[i][j]), left, top)  # 画列表1里面的值
                self.draw_number(str(li2[i][j]), left + 660, top)  # 画列表2里面的值

    # 给空列表里产生两个初始值，并画到界面
    def reset(self):
        if self.score1 > self.best_score1:
            self.best_score1 = self.score1
        if self.score2 > self.best_score2:
            self.best_score2 = self.score2
        self.score1 = 0
        self.score2 = 0
        for i in range(2):
            self.create_num1()
            self.create_num2()
        self.init_ui(0, game_list1, game_list2)     #游戏初始化的时候，没有移动列表，因此设flag为0，就不用产生新的数值了

    # 1移动一次就出现一个新的数字,game_list1
    def create_num1(self):
        while True:
            i = random.randint(0, 3)
            j = random.randint(0, 3)
            if game_list1[i][j] == ' ':
                game_list1[i][j] = random.choice([2, 2, 2, 4])
                break
            else:
                continue

    # 2移动一次就出现一个新的数字,game_list2
    def create_num2(self):
        while True:
            i = random.randint(0, 3)
            j = random.randint(0, 3)
            if game_list2[i][j] == ' ':
                game_list2[i][j] = random.choice([2, 2, 2, 4])
                break
            else:
                continue

    # 矩阵反转
    def invert(self,li):
        return [i[::-1] for i in li]

    # 矩阵转置
    def transpose(self,li):
        return [list(i) for i in zip(*li)]

    # 判断能否左移，右移，上移，下移
    def is_moving_left(self,li):
        for i in range(4):
            for j in range(3):
                if li[i][j] == ' ' and li[i][j + 1] != ' ':
                    return True
                else:
                    if li[i][j] != ' ' and li[i][j] == li[i][j + 1]:
                        return True
        else:
            return False
    def is_moving_right(self,li):
        li = self.invert(li)
        return self.is_moving_left(li)
    def is_moving_up(self,li):
        li = self.transpose(li)
        return self.is_moving_left(li)
    def is_moving_down(self,li):
        li = self.transpose(li)
        li = self.invert(li)
        return self.is_moving_left(li)

    # 进行左移，右移，上移，下移,flag的值表示移动的是第1个或第2个数值列表
    def move_left(self,flag,li):
        new_li = []
        for row in li:
            row_list = sorted(row, key=lambda x: 1 if x == ' ' else 0)
            self.add_number(flag,row_list)
            new_li.append(row_list)
        return new_li
    def move_right(self,flag,li):
        li = self.invert(li)
        li = self.move_left(flag,li)
        li = self.invert(li)
        return li
    def move_up(self,flag,li):
        li = self.transpose(li)
        li = self.move_left(flag,li)
        li = self.transpose(li)
        return li
    def move_down(self,flag,li):
        li = self.transpose(li)
        li = self.invert(li)
        li = self.move_left(flag,li)
        li = self.transpose(li)
        return li[::-1]

    #移动之后消数字：在移动方向上把两个相等的数字加起来
    def add_number(self,flag,row):
        for j in range(3):
            if row[j] != ' ' and row[j] == row[j + 1]:
                row[j] *= 2
                if flag == 1:
                    self.score1 += row[j]
                else:
                    self.score2 += row[j]
                row[j + 1] = ' '

    #判断是否有数值达到2048
    def is_get_2048(self,li):
        li = list(itertools.chain(*li))
        if max([i for i in li if i != ' ']) >= 2048:
            return True
        else:
            return False
    #判断是否能继续移动
    def is_move(self,li):
        return any((self.is_moving_left(li), self.is_moving_right(li), self.is_moving_up(li), self.is_moving_down(li)))

#游戏开始
game_list1 = []  #存放数字的空列表
game_list2 = []  #存放数字的空列表
[game_list1.append([' ' for j in range(4)]) for i in range(4)]   #利用列表生成式生成空列表（二维数组）
[game_list2.append([' ' for j in range(4)]) for i in range(4)]
game = Gamefield()  #创建游戏类的实例
game.reset()

while True:

    if game.is_move(game_list1) or game.is_move(game_list2):
        if not game.is_move(game_list1) and not game.is_get_2048(game_list1):
            game.draw_number('笨蛋，游戏失败！', 330, 850, 30, (255, 0, 0))
        elif not game.is_move(game_list1) and game.is_get_2048(game_list1):
            game.draw_number('恭喜你！其实你已经得到了2048！', 330, 850, 30, (255, 0, 0))
        elif game.is_move(game_list1) and game.is_get_2048(game_list1):
            game.draw_number('2048分已到手！继续创高分！', 330, 850, 30, (255, 0, 0))
        if not game.is_move(game_list2) and not game.is_get_2048(game_list2):
            game.draw_number('笨蛋，游戏失败！', 990, 850, 30, (255, 0, 0))
        elif not game.is_move(game_list2) and game.is_get_2048(game_list2):
            game.draw_number('恭喜你！其实你已经得到了2048！', 990, 850, 30, (255, 0, 0))
        elif game.is_move(game_list2) and game.is_get_2048(game_list2):
            game.draw_number('2048分已到手！继续创高分！', 990, 850, 30, (255, 0, 0))
    else:
        if game.is_get_2048(game_list1):
            game.draw_number('恭喜你！其实你已经得到了2048！', 330, 850, 30, (255, 0, 0))
        else:
            game.draw_number('笨蛋，游戏失败！', 330, 850, 30, (255, 0, 0))
        if game.is_get_2048(game_list2):
            game.draw_number('恭喜你！其实你已经得到了2048！', 990, 850, 30, (255, 0, 0))
        else:
            game.draw_number('笨蛋，游戏失败！', 990, 850, 30, (255, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game.draw_number('重置！游戏重新开始！', 330, 850, 30, (255, 0, 0))
                game_list1 = []
                game_list2 = []
                [game_list1.append([' ' for j in range(4)]) for i in range(4)]
                [game_list2.append([' ' for j in range(4)]) for i in range(4)]
                game.reset()
            elif event.key == pygame.K_LEFT:
                while game.is_moving_left(game_list2):
                    game_list2 = game.move_left(2,game_list2)
                game.init_ui(2,game_list1,game_list2)
            elif event.key == pygame.K_RIGHT:
                while game.is_moving_right(game_list2):
                    game_list2 = game.move_right(2,game_list2)
                game.init_ui(2,game_list1,game_list2)
            elif event.key == pygame.K_UP:
                while game.is_moving_up(game_list2):
                    game_list2 = game.move_up(2,game_list2)
                game.init_ui(2,game_list1,game_list2)
            elif event.key == pygame.K_DOWN:
                while game.is_moving_down(game_list2):
                    game_list2 = game.move_down(2,game_list2)
                game.init_ui(2,game_list1,game_list2)
            elif event.key == pygame.K_a:
                while game.is_moving_left(game_list1):
                    game_list1 = game.move_left(1,game_list1)
                game.init_ui(1,game_list1,game_list2)
            elif event.key == pygame.K_d:
                while game.is_moving_right(game_list1):
                    game_list1 = game.move_right(1,game_list1)
                game.init_ui(1,game_list1,game_list2)
            elif event.key == pygame.K_w:
                while game.is_moving_up(game_list1):
                    game_list1 = game.move_up(1,game_list1)
                game.init_ui(1,game_list1,game_list2)
            elif event.key == pygame.K_s:
                while game.is_moving_down(game_list1):
                    game_list1 = game.move_down(1,game_list1)
                game.init_ui(1,game_list1,game_list2)
    pygame.display.update()
