# 载入相关套件
import numpy as np
import pickle
import os

# 参数设定
BOARD_ROWS = 3 # 行数
BOARD_COLS = 3 # 列数

# 环境类别
class Environment:
    def __init__(self, p1, p2):
        # 变数初始化
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.p1 = p1 # 第一个玩家
        self.p2 = p2 # 第二个玩家
        self.isEnd = False    # 是否结束
        self.boardHash = None # 棋盘

        self.playerSymbol = 1 # 第一个玩家使用X

    # 记录棋盘状态
    def getHash(self):
        self.boardHash = str(self.board.reshape(BOARD_COLS * BOARD_ROWS))
        return self.boardHash

    # 判断输赢
    def is_done(self):
        # 连成一列
        for i in range(BOARD_ROWS):
            if sum(self.board[i, :]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[i, :]) == -3:
                self.isEnd = True
                return -1
                
        # 连成一行
        for i in range(BOARD_COLS):
            if sum(self.board[:, i]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[:, i]) == -3:
                self.isEnd = True
                return -1
                
        # 连成对角线
        diag_sum1 = sum([self.board[i, i] for i in range(BOARD_COLS)])
        diag_sum2 = sum([self.board[i, BOARD_COLS - i - 1] for i in 
                                                     range(BOARD_COLS)])
        diag_sum = max(abs(diag_sum1), abs(diag_sum2))
        if diag_sum == 3:
            self.isEnd = True
            if diag_sum1 == 3 or diag_sum2 == 3:
                return 1
            else:
                return -1

        # 无空位置即算平手
        if len(self.availablePositions()) == 0:
            self.isEnd = True
            return 0
        self.isEnd = False
        return None

    # 显示空位置
    def availablePositions(self):
        positions = []
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if self.board[i, j] == 0:
                    positions.append((i, j))  
        return positions

    # 更新棋盘
    def updateState(self, position):
        self.board[position] = self.playerSymbol
        # switch to another player
        self.playerSymbol = -1 if self.playerSymbol == 1 else 1

    # 给予奖励
    def giveReward(self):
        result = self.is_done()
        # backpropagate reward
        if result == 1: # 第一玩家赢，P1加一分
            self.p1.feedReward(1)
            self.p2.feedReward(0)
        elif result == -1: # 第二玩家赢，P2加一分
            self.p1.feedReward(0)
            self.p2.feedReward(1)
        else: # 胜负未分，第一玩家加 0.1分，第二玩家加 0.5分
            self.p1.feedReward(0.1)
            self.p2.feedReward(0.5)

    # 棋盘重置
    def reset(self):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1

    # 开始训练
    def play(self, rounds=100):
        for i in range(rounds):
            if i % 1000 == 0:
                print(f"Rounds {i}")
                
            while not self.isEnd:
                # Player 1
                positions = self.availablePositions()
                p1_action = self.p1.chooseAction(positions, 
                                self.board, self.playerSymbol)
                # take action and upate board state
                self.updateState(p1_action)
                board_hash = self.getHash()
                self.p1.addState(board_hash)

                # 检查是否胜负已分
                win = self.is_done()
                    
                # 胜负已分
                if win is not None:
                    self.giveReward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break
                else:
                    # Player 2
                    positions = self.availablePositions()
                    p2_action = self.p2.chooseAction(positions, 
                                    self.board, self.playerSymbol)
                    self.updateState(p2_action)
                    board_hash = self.getHash()
                    self.p2.addState(board_hash)

                    win = self.is_done()
                    if win is not None:
                        # self.showBoard()
                        # ended with p2 either win or draw
                        self.giveReward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break

    # 开始比赛
    def play2(self, start_player=1):
        is_first = True
        while not self.isEnd:
            # Player 1
            positions = self.availablePositions()
            if not (is_first and start_player==2):
                p1_action = self.p1.chooseAction(positions, 
                    self.board, self.playerSymbol)
                # take action and upate board state
                self.updateState(p1_action)
            is_first = False
            self.showBoard()
            # check board status if it is end
            win = self.is_done()
            if win is not None:
                if win == -1 or win == 1:
                    print(self.p1.name, " 胜!")
                else:
                    print("平手!")
                self.reset()
                break
            else:
                # Player 2
                positions = self.availablePositions()
                p2_action = self.p2.chooseAction(positions)

                self.updateState(p2_action)
                self.showBoard()
                win = self.is_done()
                if win is not None:
                    if win == -1 or win == 1:
                        print(self.p2.name, " 胜!")
                    else:
                        print("平手!")
                    self.reset()
                    break
    
    # 显示棋盘目前状态
    def showBoard(self):
        # p1: x  p2: o
        for i in range(0, BOARD_ROWS):
            print('-------------')
            out = '| '
            for j in range(0, BOARD_COLS):
                if self.board[i, j] == 1:
                    token = 'x'
                if self.board[i, j] == -1:
                    token = 'o'
                if self.board[i, j] == 0:
                    token = ' '
                out += token + ' | '
            print(out)
        print('-------------')

# 计算机类别
class Player:
    def __init__(self, name, exp_rate=0.3):
        self.name = name
        self.states = []  # record all positions taken
        self.lr = 0.2
        self.exp_rate = exp_rate
        self.decay_gamma = 0.9
        self.states_value = {}  # state -> value

    def getHash(self, board):
        boardHash = str(board.reshape(BOARD_COLS * BOARD_ROWS))
        return boardHash

    # 计算机依最大值函数行动
    def chooseAction(self, positions, current_board, symbol):
        if np.random.uniform(0, 1) <= self.exp_rate:
            # take random action
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            value_max = -999
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_boardHash = self.getHash(next_board)
                value = 0 if self.states_value.get(next_boardHash) is None \
                          else self.states_value.get(next_boardHash)
                
                # 依最大值函数行动
                if value >= value_max:
                    value_max = value
                    action = p
        # print("{} takes action {}".format(self.name, action))
        return action

    # 更新状态值函数
    def addState(self, state):
        self.states.append(state)

    # 重置状态值函数
    def reset(self):
        self.states = []

    # 比赛结束，倒推状态值函数
    def feedReward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr * (self.decay_gamma * reward 
                                                - self.states_value[st])
            reward = self.states_value[st]

    # 存档
    def savePolicy(self):
        fw = open(f'policy_{self.name}', 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    # 载入档案
    def loadPolicy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()

# 玩家类别
class HumanPlayer:
    def __init__(self, name):
        self.name = name
    
    # 行动
    def chooseAction(self, positions):
        while True:
            position = int(input("输入位置(1~9):"))
            row = position // 3
            col = (position % 3) - 1
            if col < 0:
                row -= 1
                col = 2
            # print(row, col)
            action = (row, col)
            if action in positions:
                return action

    # 状态值函数更新
    def addState(self, state):
        pass

    # 比赛结束，倒推状态值函数
    def feedReward(self, reward):
        pass

    def reset(self):
        pass

# 画图说明输入规则
def first_draw():
    rv = '\n'
    no=0
    for y in range(3):
        for x in range(3):
            idx = y * 3 + x
            no+=1
            rv += str(no)
            if x < 2:
                rv += '|'
        rv += '\n'
        if y < 2:
            rv += '-----\n'
    return rv

if __name__ == "__main__":  # 主程式
    import sys
    if len(sys.argv) > 1:
        start_player = int(sys.argv[1])
    else:
        start_player = 1

    # 产生物件
    p1 = Player("p1")
    p2 = Player("p2")
    env = Environment(p1, p2)
    
    # 训练
    if not os.path.exists(f'policy_p{start_player}'):
        print("开始训练...")
        env.play(50000)
        p1.savePolicy()
        p2.savePolicy()
   
    print(first_draw())  # 棋盘说明
    
    # 载入训练成果
    p1 = Player("computer", exp_rate=0)
    p1.loadPolicy(f'policy_p{start_player}')
    p2 = HumanPlayer("human")
    env = Environment(p1, p2)
    
    # 开始比赛
    env.play2(start_player)