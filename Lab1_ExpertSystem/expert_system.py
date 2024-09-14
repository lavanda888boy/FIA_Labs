from rules import LUNA_GUESTS_RULES
from production import forward_chain
from utils import QuestionGenerator

class ExpertSystem:

    def __init__(self):
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


    def traverse_goal_tree_interactively(self):
        actions = [rule._action[0] for rule in LUNA_GUESTS_RULES]
        self.identify_hypotheses(actions)
        self.identify_leaf_and_intermediary_rules(actions)

        while True: 
            existing_fact = None
            current_rule = self.get_a_new_unchecked_rule(self.leaf_rules)

            while current_rule is not None:
                facts = self.verify_rule_conditions_fulfillment(current_rule, existing_fact)
                new_facts = forward_chain(LUNA_GUESTS_RULES, facts)

                try:
                    self.mark_rule_as_checked(current_rule)
                    intermediary_fact = (new_facts - facts).pop()

                    if intermediary_fact in self.hypotheses:
                        print(f"\nThe person {' '.join(intermediary_fact.split()[1:])}")
                        return
                    else:
                        existing_fact = intermediary_fact
                        current_rule = self.get_a_new_unchecked_rule(self.intermediary_rules, intermediary_fact)

                except (KeyError):
                    if current_rule['leaf']:
                        break
                    else:
                        current_rule = self.get_a_new_unchecked_rule(self.intermediary_rules, facts[0])


    def verify_rule_conditions_fulfillment(self, rule, existing_fact):
        facts = set()
        conditions = rule['rule']._conditional.conditions()

        if existing_fact is not None:
            facts.add(existing_fact)

            if 'OR' in str(type(rule['rule']._conditional)):
                return facts
            
            response = self.ask_conditional_question(conditions[1])
            if response.startswith("Yes"):
                facts.add(conditions[1])
        else:
            first_response = self.ask_conditional_question(conditions[0])
            if first_response.startswith("Yes"):
                facts.add(conditions[0])
                
                if 'OR' in str(type(rule['rule']._conditional)):
                    return facts
            else:
                if 'AND' in str(type(rule['rule']._conditional)):
                    return facts
                
            second_response = self.ask_conditional_question(conditions[1])
            if second_response.startswith("Yes"):
                facts.add(conditions[1])
        
        return facts

 
    def ask_conditional_question(self, condition):
        question = self.question_generator.generate_yes_no_question(condition)
        print(f"\n{question}")
        user_response = input("\nYes/No? ")

        while (not user_response.startswith("Yes")) and (not user_response.startswith("No")):
            user_response = input("\nYes/No? ")
        
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