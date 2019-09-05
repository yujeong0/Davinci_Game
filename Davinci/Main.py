import numpy.random
from Player import Player
from Block import Block

class main:
    def __init__(self):
        self.players = None
        self.blocks = [False] * 26   # 검은색숫자 0~11 (조커 : 24)  흰색 12~23 (조커 : 25)
        self.play_order = -1
        self.num_of_blocks = 0       # 플레이어 당 가지고 있는 블록 수

    def start(self):
        print("다빈치 코드 게임을 시작합니다.")
        print("플레이어 수 : ", end= "")
        num_of_players = int(input())
        if num_of_players > 3:
            self.num_of_blocks = 3
        else: self.num_of_blocks = 4

        self.players = [''] * num_of_players
        for i in range(0, num_of_players):
            print("플레이어{} 이름 : ".format(i+1), end="")
            name = input()
            player_block = self._distributing_init_blocks()
            self.players[i] = Player(name, self.num_of_blocks, player_block)
            self.players[i]._sorting_blocks()

    def _distributing_init_blocks(self):        # 플레이어들에게 블록 초기 분배
        blocks = [None] * self.num_of_blocks
        count = 0
        while True:
            if count >= self.num_of_blocks: break
            num = numpy.random.randint(24, size=1)[0] # 0에서 23까지 블록 할당(조커 제외)
            if self.blocks[num]: continue     # 이미 다른 플레이어가 가지고 있는 블록이면(True이면) 다시 뽑기
            self.blocks[num] = True

            if num < 12:
                color = "black"
                if num == 24: num = 12
            else:
                color = "white"
                num -= 12

            blocks[count] = Block(num, color)
            count += 1

        return blocks

    @staticmethod
    def random_check(numlist, number):  #블록 랜덤 선택할 때 중복 체크
        for i in range(len(numlist)):
            if numlist[i] == number:
                return False
        return True

    def _setting_the_order(self):   #플레이어들 진행 순서 임의로 정하기
        numpy.random.shuffle(self.players)
        self.play_order = 0

    def run(self):
        self.start()
        self._setting_the_order()
        while True:
            self._reasoning()
            if self._searching_winner():
                break
            self.reporting()

    def _giving_a_block(self):      #방금 뽑은 블록 반환
        print("블록을 하나 뽑았습니다.")
        while True:
            num = numpy.random.randint(26, size=1)[0]
            if self.blocks[num] == False:  # 이미 다른 플레이어가 가지고 있는 블록이면(True이면) 다시 뽑기
                break

        self.blocks[num] = True
        if num < 12 or num == 24:
            color = "black"
            if num == 24: num = 12
        else:
            color = "white"
            if num == 25: num = 12
            else: num -= 12

        b = Block(num, color)
        self.players[self.play_order]._blocks.append(b)
        self.players[self.play_order].blocks_list.append(False)
        self.players[self.play_order]._sorting_blocks()

        return b

    def _reasoning(self):
        if self.play_order == len(self.players):
            self.play_order = 0

        print(self.players[self.play_order].get_name() + "님의 차례입니다.")
        b = self._giving_a_block()
        self.players[self.play_order].reporting_mine()
        self.reporting()

        while True:
            attacked_player = None
            print("추리할 플레이어 이름 입력하삼 : ", end="")
            while True:
                name = input()
                findname = False
                for player in self.players:
                    if name == player.get_name():
                        findname = True
                        attacked_player = player
                        break

                if findname == False: print("이름 다시 입력하셈 : ", end="")
                else: break

            while True:
                print("몇 번째 블록을 맞출 건지 입력하셈 : ", end="")
                index = input()
                if index.isdecimal():
                    index = int(index) - 1
                    if len(attacked_player._blocks)-1 < index:
                        print("유효한 블록이 아니지롱")
                        continue
                    else: break
                else:
                    print("숫자 입력하셈 ㅡㅡ")
                    continue

            while True:
                print("숫자(숫자 0~11, 조커:12)입력하셈 : ", end="")
                num = input()
                if num.isdecimal():
                    num = int(num)
                    if num < 0 and num > 12:
                        print("유효한 숫자가 아니지롱")
                        continue
                    else: break
                else:
                    print("숫자 입력하셈 ㅡㅡ")
                    continue

            if attacked_player.matching_block_number(index, num):
                print("추측 성공! 축하 ^0^")
                attacked_player.blocks_list[index] = True
                attacked_player.reporting_block_list()
                print("또 추측하려면 1, 차례를 넘기려면 2를 입력하삼! : ", end="")
                tmp = int(input())
                if tmp == 2:
                    self.play_order += 1
                    break

            else:
                print("추측 실패ㅠ 블록을 공개합니다ㅠ")
                self.players[self.play_order].openning_the_blocks(b)
                self.play_order += 1
                break

    def reporting(self):
        count = 0
        for i in self.blocks:
            if i == False: count += 1

        print("---게임 현황---")
        print("남은 블록 수 : {}개".format(count))
        print("남은 플레이어 수 : {}명".format(len(self.players)))

        for player in self.players:
            player.reporting_block_list()

    def _searching_winner(self):
        list = []
        for i in range(len(self.players)):
            open = True
            for tmp in self.players[i].blocks_list:
                if tmp == False:
                    open = False
                    break
            if open:    #모든 블록이 공개된 플레이어 제외
                list.append(i)

        for i in range(len(list)):
            del self.players[i]

        if len(self.players) == 1:  # 플레이어가 최종으로 한 명이 남으면
            self.reporting()
            print("승리자는 " + self.players[0].get_name() + "입니다! 축하!^0^")
            return True

        return False

davinch = main()
davinch.run()