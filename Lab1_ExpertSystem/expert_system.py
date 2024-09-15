from rules import LUNA_GUESTS_RULES
from production import forward_chain, backward_chain
from utils import QuestionGenerator

from random import randint

class ExpertSystem:

    def __init__(self):
        self.actions = []
        self.leaf_rules = []
        self.intermediary_rules = []
        self.hypotheses = []
        self.question_generator = QuestionGenerator()

    
    def identify_hypotheses(self, actions):
        for action in actions:
            invalid_action = False

            for rule in LUNA_GUESTS_RULES:
                if action in rule._conditional.conditions():
                    invalid_action = True
                    break
            
            if not invalid_action:
                self.hypotheses.append(action)

    
    def get_person_category_encyclopedia_view(self):
        if len(self.actions) == 0:
            self.actions = [rule._action[0] for rule in LUNA_GUESTS_RULES]

        if len(self.hypotheses) == 0:
            self.identify_hypotheses(self.actions)

        hypothesis = input("\nEnter your hypothesis (for example, 'Tim is a Student'): ")
        words = hypothesis.split()
        words[0] = '(?x)'
        hypothesis_action = ' '.join(words)

        while hypothesis_action not in self.hypotheses:
            print("\nThe system does not recognize the hypothesis")
            hypothesis = input("\nTry again (for example, 'Tim is a Student'): ")

        print()
        backward_chain(LUNA_GUESTS_RULES, hypothesis, hypothesis.split()[0], verbose=True)


    def identify_leaf_and_intermediary_rules(self, actions):
        for rule in LUNA_GUESTS_RULES:
            invalid_condition = False

            for condition in rule._conditional.conditions():
                if condition in actions:
                    invalid_condition = True
                    self.intermediary_rules.append({'rule': rule, 'checked': False, 'leaf': False})
                    break
            
            if not invalid_condition:
                self.leaf_rules.append({'rule': rule, 'checked': False, 'leaf': True})


    def get_a_new_unchecked_rule(self, rules, existing_fact=None):
        for rule in rules:
            if not rule['checked']:
                if (existing_fact is None) or (existing_fact in rule['rule']._conditional.conditions()):
                    return rule
        return None


    def get_list_of_unchecked_rules(self, rules, existing_fact):
        aggregated_rules = []

        for rule in rules:
            if not rule['checked']:
                if existing_fact in rule['rule']._conditional.conditions():
                    aggregated_rules.append(rule)

        return aggregated_rules


    def traverse_goal_tree_interactively(self):
        if len(self.actions) == 0:
            self.actions = [rule._action[0] for rule in LUNA_GUESTS_RULES]

        if len(self.hypotheses) == 0:
            self.identify_hypotheses(self.actions)

        self.identify_leaf_and_intermediary_rules(self.actions)

        while True: 
            existing_fact = None
            current_rule = self.get_a_new_unchecked_rule(self.leaf_rules)

            if current_rule is None:
                print("\nThe person cannot be identified by the system")
                return
            
            choice_facts = None

            while current_rule is not None:
                if choice_facts is not None:
                    facts = choice_facts
                else:
                    facts = self.verify_single_condition_fulfillment(current_rule, existing_fact)
                
                new_facts = forward_chain(LUNA_GUESTS_RULES, facts)
                self.mark_rule_as_checked(current_rule)

                try:
                    intermediary_fact = (new_facts - facts).pop()

                    if intermediary_fact in self.hypotheses:
                        print(f"\nThe person {' '.join(intermediary_fact.split()[1:])}")
                        return
                    else:
                        existing_fact = intermediary_fact
                        curr_rules = self.get_list_of_unchecked_rules(self.intermediary_rules, existing_fact)

                        if len(curr_rules) > 1:
                            choice_facts = self.verify_multiple_conditions_fulfillment(curr_rules, existing_fact)
                            for rule in curr_rules:
                                self.mark_rule_as_checked(rule)
                        else:
                            current_rule = curr_rules[0]

                except (KeyError):
                    if current_rule['leaf']:
                        break
                    else:
                        current_rule = self.get_a_new_unchecked_rule(self.intermediary_rules, list(facts)[0])


    def verify_single_condition_fulfillment(self, rule, existing_fact):
        facts = set()
        conditions = rule['rule']._conditional.conditions()

        if existing_fact is not None:
            facts.add(existing_fact)

            if 'OR' in str(type(rule['rule']._conditional)):
                return facts
            
            response = self.ask_single_choice_question(conditions[1])
            if response.startswith("Yes"):
                facts.add(conditions[1])
        else:
            first_response = self.ask_single_choice_question(conditions[0])
            if first_response.startswith("Yes"):
                facts.add(conditions[0])
                
                if 'OR' in str(type(rule['rule']._conditional)):
                    return facts
            else:
                if 'AND' in str(type(rule['rule']._conditional)):
                    return facts
                
            second_response = self.ask_single_choice_question(conditions[1])
            if second_response.startswith("Yes"):
                facts.add(conditions[1])
        
        return facts
    

    def verify_multiple_conditions_fulfillment(self, rules, existing_fact):
        facts = set()
        facts.add(existing_fact)

        conditions = []
        for rule in rules:
            conditions.append(rule['rule']._conditional.conditions()[1])

        question_choice = randint(1, 3)

        if question_choice != 1:
            response = self.ask_multiple_choice_question(conditions)

            if response != len(conditions) + 1:
                facts.add(conditions[response - 1])
        else:
            response = self.ask_user_input_question()

            for condition in conditions:
                if condition.endswith(response):
                    facts.add(condition)
                    break

        return facts

 
    def ask_single_choice_question(self, condition):
        question = self.question_generator.generate_yes_no_question(condition)
        print(f"\n{question}")
        user_response = input("\nYes/No? ")

        while (not user_response.startswith("Yes")) and (not user_response.startswith("No")):
            user_response = input("\nYes/No? ")
        
        return user_response
    

    def ask_multiple_choice_question(self, conditions):
        question = self.question_generator.generate_multiple_choice_question(conditions)
        print(f"\n{question}")
        user_response = int(input("\nChoose an option: "))

        while not user_response in [option for option in range(1, len(conditions) + 2)]:
            user_response = int(input("\nChoose an option: "))
        
        return user_response
    

    def ask_user_input_question(self):
        question = self.question_generator.generate_user_input_question()
        print(f"\n{question}")
        user_response = input("\nYour insight: ")

        return user_response
    

    def mark_rule_as_checked(self, checked_rule):
        rules = []
        if checked_rule['leaf']:
            rules = self.leaf_rules  
        else:
            rules = self.intermediary_rules

        for rule in rules:
            if rule['rule'].__str__().startswith(checked_rule['rule'].__str__()):
                rule['checked'] = True
                return