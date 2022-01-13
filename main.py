# 现有bug：碰撞检测不完善
# 需添加的功能：
# decode = 'utf-8'
import pygame
import sys
from pygame.locals import *
import random
import math
import easygui

import wordcloud


time = 0  # 定义每次游戏开始的时间
bgm_index = 0  # 定义背景音乐播放


class board(pygame.sprite.Sprite):  # 定义挡板类
    def __init__(self, image, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()  # 引进板子
        self.mouse_rect = self.image.get_rect()  # 找到位置
        self.mouse_rect.left, self.mouse_rect.top = bg_size[0] // 2 - self.image.get_rect().width // 2, bg_size[
            1] * 3 // 4  # 设置起始位置
        pygame.mouse.set_visible(False)  # 设置鼠标不可见


class Ball(pygame.sprite.Sprite):  # 定义球类
    def __init__(self, image, speed, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = speed
        self.width, self.height = bg_size[0], bg_size[1]
        self.bg_size = bg_size

    def move(self, speed):  # 传入速度让球动起来
        self.rect = self.rect.move(self.speed)


def write(content, color, size):  # 字符显示
    for i in pygame.font.get_fonts():
        if '宋' in i or '华' in i:
            temp = i
    font = pygame.font.SysFont(temp, size)
    text = font.render(content, True, pygame.Color(color[0], color[1], color[2]))
    return text


def main1():  # 函数主体
    global time  # 游戏开始的时间
    global bgm_index

    pygame.mixer.pre_init(frequency=44100)
    pygame.init()
    pygame.font.init()
    pygame.mixer.init(frequency=44100)

    bgm1 = pygame.mixer.music  # 设置背景音乐和碰撞音效
    if bgm_index == 0:
        bgm1.load('windy hill.mp3')
    elif bgm_index == 1:
        bgm1.load('SawanoHiroyuki[nZk] (泽野弘之) _ 瑞葵 (mizuki) - aLIEz.mp3')
    elif bgm_index == 2:
        bgm1.load('毛华锋 - 奇迹再现.mp3')
    elif bgm_index == 3:
        bgm1.load('约瑟翰 庞麦郎 - 我的滑板鞋.mp3')
    elif bgm_index == 4:
        bgm1.load('久石让 - Merry-Go-Round.mp3')
    bgm1.set_volume(0.4)
    bgm1.play(-1)  # 重复播放

    peng = pygame.mixer.Sound('弹球音效.mp3')
    peng.set_volume(1.5)

    pygame.display.set_caption('休闲游戏：弹球')
    bg_size1 = width, height = 1000, 700
    screen = pygame.display.set_mode(bg_size1)
    board1 = board('board.png', bg_size1)
    speed = [random.uniform(1, 3), random.uniform(1, 3)]  # 初始速度
    ball1 = Ball('ball.png', speed, bg_size1)
    group = [board1]
    flag = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    pause = False
    index = 0  # 标记当前速度阶段
    point = 0
    bg = pygame.image.load('grass.jpg')
    n = 0  # 撞挡板时的额外分数
    flag1 = 0  # 判断是否要发声
    flag2 = False  # 用于判断暂停时音乐是否切换
    temp0 = 0  # 用于空格时暂停记分
    temp1 = 0  # 用于记录真实的游戏时间

    clock = pygame.time.Clock()  # 定义clock用于计时
    clock1 = pygame.time.Clock()  # 用于魔鬼阶段计时

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    pygame.mixer.init()
                    bgm_index = (bgm_index + 4) % 5
                    if bgm_index == 0:
                        bgm1.load('windy hill.mp3')
                        if not pause:
                            bgm1.play(-1)
                        else:
                            flag2 = True  # 用于判断暂停时音乐是否切换
                    elif bgm_index == 1:
                        bgm1.load('SawanoHiroyuki[nZk] (泽野弘之) _ 瑞葵 (mizuki) - aLIEz.mp3')
                        bgm1.set_volume(0.4)
                        if not pause:
                            bgm1.play(-1)
                        else:
                            flag2 = True  # 用于判断暂停时音乐是否切换
                    elif bgm_index == 2:
                        bgm1.load('毛华锋 - 奇迹再现.mp3')
                        bgm1.set_volume(0.4)
                        if not pause:
                            bgm1.play(-1)
                        else:
                            flag2 = True  # 用于判断暂停时音乐是否切换
                    elif bgm_index == 3:
                        bgm1.load('约瑟翰 庞麦郎 - 我的滑板鞋.mp3')
                        bgm1.set_volume(0.4)
                        if not pause:
                            bgm1.play(-1)
                        else:
                            flag2 = True  # 用于判断暂停时音乐是否切换
                    elif bgm_index == 4:
                        bgm1.load('久石让 - Merry-Go-Round.mp3')
                        bgm1.set_volume(0.4)
                        if not pause:
                            bgm1.play(-1)
                        else:
                            flag2 = True  # 用于判断暂停时音乐是否切换
                elif event.key == K_RIGHT:
                    pygame.mixer.init()
                    bgm_index = (bgm_index + 1) % 5
                    if bgm_index == 0:
                        bgm1.load('windy hill.mp3')
                        if not pause:
                            bgm1.play(-1)
                        else:
                            flag2 = True  # 用于判断暂停时音乐是否切换
                    elif bgm_index == 1:
                        bgm1.load('SawanoHiroyuki[nZk] (泽野弘之) _ 瑞葵 (mizuki) - aLIEz.mp3')
                        bgm1.set_volume(0.4)
                        if not pause:
                            bgm1.play(-1)
                        else:
                            flag2 = True  # 用于判断暂停时音乐是否切换
                    elif bgm_index == 2:
                        bgm1.load('毛华锋 - 奇迹再现.mp3')
                        bgm1.set_volume(0.4)
                        if not pause:
                            bgm1.play(-1)
                        else:
                            flag2 = True  # 用于判断暂停时音乐是否切换
                    elif bgm_index == 3:
                        bgm1.load('约瑟翰 庞麦郎 - 我的滑板鞋.mp3')
                        bgm1.set_volume(0.4)
                        if not pause:
                            bgm1.play(-1)
                        else:
                            flag2 = True  # 用于判断暂停时音乐是否切换
                    elif bgm_index == 4:
                        bgm1.load('久石让 - Merry-Go-Round.mp3')
                        bgm1.set_volume(0.4)
                        if not pause:
                            bgm1.play(-1)
                        else:
                            flag2 = True  # 用于判断暂停时音乐是否切换

                if event.key == K_SPACE:  # 当按下空格键时暂停游戏
                    pause = not pause
                    if pause:
                        bgm1.pause()
                        temp0 = pygame.time.get_ticks() - time
                    else:
                        if flag2:
                            bgm1.play()
                            flag2 = False  # 重置flag2
                        else:
                            bgm1.unpause()
                        temp1 += pygame.time.get_ticks() - time - temp0

        if not pause:  # 当暂停时显示鼠标并停止移动滑板
            board1.mouse_rect.left, board1.mouse_rect.top = pygame.mouse.get_pos()[0], bg_size1[1] * 3 // 4
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)
        if board1.mouse_rect.left <= 0:  # 判断鼠标是否越界
            board1.mouse_rect.left = 0
        if board1.mouse_rect.left >= bg_size1[0] - board1.mouse_rect.width:
            board1.mouse_rect.left = bg_size1[0] - board1.mouse_rect.width

        if ball1.rect.left < 0 or ball1.rect.right >= bg_size1[0]:  # 边界反弹
            flag1 = 1  # 判断是否要发声
            speed[0] = -speed[0]
        if ball1.rect.top < 0 or ball1.rect.bottom >= bg_size1[1]:
            flag1 = 1  # 判断是否要发声
            speed[1] = -speed[1]

        group[0].rect = group[0].mouse_rect
        if pygame.sprite.spritecollide(ball1, group, False):  # 碰撞检测
            flag1 = 1  # 判断是否要发声
            n += 1000  # 撞挡板时的额外分数
            speed[1] = -speed[1]
        if ball1.rect.bottom >= bg_size1[1]:
            pygame.mixer.music.pause()
            running = False

        if pygame.time.get_ticks() - temp1 - time > 5000 and flag[0] and not pause:  # 加速
            index = 1
            speed[0] += random.random() * speed[0] / math.fabs(speed[0])
            speed[1] += random.random() * speed[1] / math.fabs(speed[1])
            flag[0] = 0
        elif pygame.time.get_ticks() - temp1 - time > 10000 and flag[1] and not pause:
            index = 2
            speed[0] += random.random() * speed[0] / math.fabs(speed[0])
            speed[1] += random.random() * speed[1] / math.fabs(speed[1])
            flag[1] = 0
        elif pygame.time.get_ticks() - temp1 - time > 15000 and flag[2] and not pause:
            index = 3
            speed[0] += random.random() * speed[0] / math.fabs(speed[0])
            speed[1] += random.random() * speed[1] / math.fabs(speed[1])
            flag[2] = 0
        elif pygame.time.get_ticks() - temp1 - time > 20000 and flag[3] and not pause:
            index = 4
            speed[0] += random.random() * speed[0] / math.fabs(speed[0])
            speed[1] += random.random() * speed[1] / math.fabs(speed[1])
            flag[3] = 0
        elif pygame.time.get_ticks() - temp1 - time > 25000 and flag[4] and not pause:
            index = 5
            speed[0] += random.random() * speed[0] / math.fabs(speed[0]) * 2
            speed[1] += random.random() * speed[1] / math.fabs(speed[1]) * 2
            flag[4] = 0
        elif pygame.time.get_ticks() - temp1 - time > 30000 and flag[5] and not pause:
            index = 6
            speed[0] += random.random() * speed[0] / math.fabs(speed[0]) * 2
            speed[1] += random.random() * speed[1] / math.fabs(speed[1]) * 2
            flag[5] = 0
        elif pygame.time.get_ticks() - temp1 - time > 35000 and flag[6] and not pause:
            index = 7
            speed[0] += random.random() * speed[0] / math.fabs(speed[0]) * 2
            speed[1] += random.random() * speed[1] / math.fabs(speed[1]) * 2
            flag[6] = 0
        elif pygame.time.get_ticks() - temp1 - time > 40000 and flag[7] and not pause:
            index = 8
            speed[0] += random.random() * speed[0] / math.fabs(speed[0]) * 2
            speed[1] += random.random() * speed[1] / math.fabs(speed[1]) * 2
            flag[7] = 0
        elif pygame.time.get_ticks() - temp1 - time > 45000 and flag[8] and not pause:
            index = 9
            speed[0] += random.random() * speed[0] / math.fabs(speed[0]) * 2
            speed[1] += random.random() * speed[1] / math.fabs(speed[1]) * 2
            flag[8] = 0
        elif pygame.time.get_ticks() - temp1 - time > 50000 and flag[9] and not pause:
            index = 10
            speed[0] += random.random() * speed[0] / math.fabs(speed[0]) * 2
            speed[1] += random.random() * speed[1] / math.fabs(speed[1]) * 2
            flag[9] = 0
        elif pygame.time.get_ticks() - temp1 - time > 55000 and flag[10] and not pause:
            index = 11
        if index == 11 and not pause and math.fabs(speed[0]) < 18 and math.fabs(speed[1]) < 18:  # 魔鬼阶段的随机变速
            speed[0] += (random.random() - 0.5) * speed[0] / math.fabs(speed[0]) * 3
            speed[1] += (random.random() - 0.5) * speed[1] / math.fabs(speed[1]) * 3
        elif index == 11 and not pause and (math.fabs(speed[0]) > 18 or math.fabs(speed[1]) > 18):
            speed[0] += (random.random() - 1) * speed[0] / math.fabs(speed[0]) * 3
            speed[1] += (random.random() - 1) * speed[1] / math.fabs(speed[1]) * 3
        if not pause:
            # 完善最后的bug：
            check = 0  # 用于检测球和四壁重复碰撞时人为移动的次数
            if ball1.rect.top < -5:
                while ball1.rect.top < 0:
                    ball1.move([0, 3])
                    check += 1
                    if check > 10:
                        break
            if ball1.rect.right > bg_size1[0] + 5:
                while ball1.rect.right > bg_size1[0]:
                    ball1.move([-3, 0])
                    check += 1
                    if check > 10:
                        break
            if ball1.rect.left < -5:
                while ball1.rect.left < 0:
                    ball1.move([3, 0])
                    check += 1
                    if check > 10:
                        break

            point = (pygame.time.get_ticks() - temp1 - time) // 10 + n
            ball1.move(speed)  # 变换球的速度后球开始动

        screen.fill((255, 255, 255))
        screen.blit(write('欢迎来玩我的游戏！', [117, 207, 241], 38), (350, 605))
        screen.blit(write('当前分数：{:,}'.format(point), [247, 59, 68], 30), (366, 650))
        screen.blit(write('操作指南', [0, 0, 0], 30), (5, 603))
        screen.blit(write('空格：暂停', [0, 0, 0], 20), (30, 640))
        screen.blit(write('左右方向键：切换背景音乐', [0, 0, 0], 20), (30, 666))
        if index == 11 or index == 12:
            screen.blit(write('当前速度阶段：魔鬼', [247, 59, 68], 22), (bg_size1[0] - 200, bg_size1[1] - 80))
        else:
            screen.blit(write('当前速度阶段：{}'.format(index), [0, 0, 0], 18), (bg_size1[0] - 200, bg_size1[1] - 80))
        screen.blit(write('当前帧率：{:.6f}'.format(clock.get_fps()), [0, 0, 0], 15), (bg_size1[0] - 190, bg_size1[1] - 18))
        if clock.get_fps() <= 50:
            screen.blit(write('当前帧率过低，可能会引起游戏卡顿！', [247, 59, 68], 15), (bg_size1[0] - 435, bg_size1[1] - 18))
        screen.blit(write('当前速度：[{:.2f},{:.2f}]'.format(speed[0], speed[1]), [0, 0, 0], 15),
                    (bg_size1[0] - 190, bg_size1[1] - 35))
        if bgm_index == 0:
            screen.blit(write('正在播放：windy hills', [0, 0, 0], 15), (bg_size1[0] - 190, bg_size1[1] - 52))
            bg = pygame.image.load('grass.jpg')
            screen.blit(pygame.transform.scale(bg, (1000, 600)), (0, 0))
        elif bgm_index == 1:
            screen.blit(write('正在播放：aLIEz', [0, 0, 0], 15), (bg_size1[0] - 190, bg_size1[1] - 52))
            bg = pygame.image.load('alize.jpg')
            screen.blit(pygame.transform.scale(bg, (1000, 600)), (0, 0))
        elif bgm_index == 2:
            screen.blit(write('正在播放：奇迹再现', [0, 0, 0], 15), (bg_size1[0] - 190, bg_size1[1] - 52))
            bg = pygame.image.load('奥特曼.jpg')
            screen.blit(pygame.transform.scale(bg, (1000, 600)), (0, 0))
        elif bgm_index == 3:
            screen.blit(write('正在播放：我的滑板鞋', [0, 0, 0], 15), (bg_size1[0] - 190, bg_size1[1] - 52))
            bg = pygame.image.load('滑板鞋.jpg')
            screen.blit(pygame.transform.scale(bg, (1000, 600)), (0, 0))
        elif bgm_index == 4:
            screen.blit(write('正在播放：merry go round', [0, 0, 0], 15), (bg_size1[0] - 190, bg_size1[1] - 52))
            bg = pygame.image.load('merry go round.png')
            screen.blit(pygame.transform.scale(bg, (1000, 600)), (0, 0))

        screen.blit(ball1.image, ball1.rect)
        screen.blit(board1.image, board1.mouse_rect)
        if flag1 == 1:
            peng.set_volume(0.3 * index)
            peng.play()
            flag1 = 0

        pygame.display.flip()
        clock.tick(70)
    a = easygui.buttonbox('您输了！\n是否重新开始游戏？', '结束', ('再来一次', '不玩了不玩了'))
    if a == '再来一次':
        pygame.init()
        time = pygame.time.get_ticks() - temp1
        main1()
    else:
        c = easygui.buttonbox('主人真的要离开孩子吗？‘（＋﹏＋）′', '结束', ('走了走了', '不我还想陪你'))
        if c == '不我还想陪你':
            pygame.init()
            time = pygame.time.get_ticks() - temp1
            main1()
        else:
            easygui.msgbox('我一定乖乖的在这里等着主人的归来哦！&( ^__^ )&')


if __name__ == '__main__':
    b = easygui.buttonbox('一款超休闲的小游戏！\n作者：迷失的蓝色小恐龙', '开始', ('开始游戏', '游戏介绍（建议先看）', '退出'))
    while b != '开始游戏':
        if b != '游戏介绍（建议先看）':
            break
        easygui.msgbox(
            '      首先欢迎来玩我的小游戏！游戏是用python语言写的，\n本萌新第一次写游戏，大佬不喜勿喷。\n\n      游戏介绍：\n   本游戏就是最经典的弹球游戏的复刻，目标很简单：移动你的鼠标控制挡板，不要让你的小球掉下去！\n   空格键暂停，左右方向键切换背景音乐！\n   本游戏分为11个阶段，1-10阶段会随机加速，11阶段为魔鬼阶段，会随机变速！\n评分标准：分数会随时间增长而增长，小球撞到挡板会有1000分的加分！\n建议：一定要坚持到魔鬼阶段呦！加油吧！',
            '游戏介绍')
        b = easygui.buttonbox('一款超休闲的小游戏！\n作者：迷失的蓝色小恐龙', '开始', ('开始游戏', '游戏介绍（建议先看）', '退出'))
    if b == '开始游戏':
        main1()
