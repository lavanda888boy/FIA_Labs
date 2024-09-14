from rules import LUNA_GUESTS_RULES
from production import forward_chain, backward_chain
from utils import QuestionGenerator

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

            while current_rule is not None:
                facts = self.verify_rule_conditions_fulfillment(current_rule, existing_fact)

                new_facts = forward_chain(LUNA_GUESTS_RULES, facts)
                self.mark_rule_as_checked(current_rule)

                try:
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
                        current_rule = self.get_a_new_unchecked_rule(self.intermediary_rules, list(facts)[0])


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