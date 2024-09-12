# TODO: add your imports here:
from rules import LUNA_GUESTS_RULES
from production import forward_chain, backward_chain, AND, OR
from utils import QuestionGenerator
from expert_system import ExpertSystem

if __name__=='__main__':

    #TODO: implement your code here!
    
    print("Welcome to Luna City Tourist Expert System!")

    es = ExpertSystem()
    es.traverse_goal_tree_interactively()