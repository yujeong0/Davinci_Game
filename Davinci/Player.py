from Block import Block
import numpy.random

class Player:

    def __init__(self, name="", num_of_blocks=0, blocks=None):
        self.name = name
        self._blocks = blocks
        self.blocks_list = [False] * num_of_blocks  #블록 공개 여부


    def _sorting_blocks(self):
        self._blocks.sort(key= lambda Block : Block._number)
        for i in range(0, len(self._blocks)-2, 2):
            if self._blocks[i]._number == self._blocks[i + 1]._number and self._blocks[i]._color == "white" and self._blocks[i + 1]._color == "black":
               self._blocks[i], self._blocks[i + 1] = self._blocks[i + 1], self._blocks[i]

        if self._blocks[len(self._blocks)-1]._number == 12:
            num = numpy.random.randint(len(self._blocks)-1, size=1)
            self._blocks[len(self._blocks)-1], self._blocks[num] = self._blocks[num], self._blocks[len(self._blocks)-1]

    def openning_the_blocks(self, block):
        for i in range(len(self._blocks)):
            if self._blocks[i]._number == block._number and self._blocks[i]._color == block._color:
                self.blocks_list[i] = True

    def matching_block_number(self, index, num):
        if self._blocks[index]._number == num:
            return True
        return False

    def reporting_mine(self):
        print(self.name + " 나의 블록")
        for i in range(len(self._blocks)):
            if self._blocks[i]._color == "white":
                print("{}w".format(self._blocks[i]._number), end=" ")
            else:
                print("{}b".format(self._blocks[i]._number), end=" ")
        print()


    def reporting_block_list(self):
        print(self.name + "님의 블록")
        for i in range(len(self.blocks_list)):
            if self.blocks_list[i]:
                if self._blocks[i]._color == "white":
                    print("{}w".format(self._blocks[i]._number), end=" ")
                else: print("{}b".format(self._blocks[i]._number), end=" ")

            else:
                if self._blocks[i]._color == "white":
                    print("w", end=" ")
                else:
                    print("b", end=" ")

        print()
        print()

    def get_name(self):
        return self.name
