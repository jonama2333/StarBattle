from MCTS import MCTS
from copy import *
from StarBattle import *

#instance_string = "1222211134111341555415555"
instance_string = ("11111123333334"+"11221122223334"+"15522222622334"+"15555662622334"+"11575662623344"+"75575666628399"+"7557566A668999"+"7777566AA88989"+"BB7CCCCAAA8889"+"B77CCCCA888989"+"BBCCCCCA889999"+"BBBDCCCAA88999"+"BBDDDDAAA8EEE9"+"BDDDDDEEEEEEEE")
#instance_string = "11223333"+"11122333"+"11223344"+"11533334"+"15555366"+"17775336"+"11173333"+"11778888"
#instance_string = "1111112222"+"1113342222"+"1111344444"+"5333334444"+"5533333446"+"5577338666"+"5577778666"+"5597778666"+"5597888AAA"+"5997888AAA"
print(len(instance_string))

board = Board(instance_str=instance_string, m=14, n=14, k=14, star=3)
init_state = Decision(board)

#mcts = MCTS(exploration_parameter=10000000000, time_limit=60)
mcts = MCTS(time_limit=600)
mcts.play(init_state, board)