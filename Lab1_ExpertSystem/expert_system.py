from rules import LUNA_GUESTS_RULES
from production import forward_chain
from utils import QuestionGenerator

class ExpertSystem:

    def __init__(self):
        self.leaf_rules = []
        self.intermediary_rules = []
        self.question_generator = QuestionGenerator()


    def identify_leaf_and_intermediary_rules(self):
        actions = []
        for rule in LUNA_GUESTS_RULES:
            actions.append(rule._action[0])

        for rule in LUNA_GUESTS_RULES:
            invalid_condition = False

            for condition in rule._conditional.conditions():
                if condition in actions:
                    invalid_condition = True
                    self.intermediary_rules.append({'rule': rule, 'status': 'unchecked'})
                    break
            
            if not invalid_condition:
                self.leaf_rules.append({'rule': rule, 'status': 'unchecked'})


    def unchecked_rules_exist(self, rules):
        for rule in rules:
            if rule['status'].startswith('unchecked'):
                return rule
        return None


    def traverse_goal_tree_interactively(self):
        self.identify_leaf_and_intermediary_rules()

        while True: 
            current_rule = self.unchecked_rules_exist(self.leaf_rules)

            while current_rule is not None:
                facts = self.verify_rule_conditions_fulfillment(current_rule)
                new_facts = forward_chain(LUNA_GUESTS_RULES, facts)

                try:
                    intermediary_fact = (new_facts - facts).pop()
                except KeyError as err:
                    print(err)


    def verify_rule_conditions_fulfillment(self, rule):
        fact_list = set()
        conditions = rule['rule']._conditional.conditions()
        
        first_response = self.ask_conditional_question(conditions[0])
        if first_response.startswith("Yes"):
            fact_list.add(conditions[0])
            
            if 'OR' in str(type(rule['rule']._conditional)):
                return fact_list
            
        elif 'AND' in str(type(rule['rule']._conditional)):
            return fact_list
            
        second_response = self.ask_conditional_question(conditions[1])
        if second_response.startswith("Yes"):
            fact_list.add(conditions[1])
        
        return fact_list


    def ask_conditional_question(self, condition):
        question = self.question_generator.generate_yesno_question(condition)
        print(f"\n{question}")
        user_response = input("\nYes/No? ")

        while (not user_response.startswith("Yes")) and (not user_response.startswith("No")):
            user_response = input("\nYes/No? ")
        
        return user_response
    
    def mark_fact_as_checked(self, fact):
        pass