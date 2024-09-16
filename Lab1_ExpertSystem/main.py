from expert_system import ExpertSystem

if __name__=='__main__':
    print("Welcome to Luna City Tourist Expert System!")

    while True:
        request = int(input("\nChoose expert system mode:\n1 - person identification\n2 - encyclopedia view\n3 - exit\n\n"))

        while request not in [1, 2, 3]:
            request = int(input("\nChoose expert system mode:\n1 - person identification\n2 - encyclopedia view\n\n"))
        
        es = ExpertSystem()
        if request == 1:
            es.traverse_goal_tree_interactively()
        elif request == 2:
            es.get_person_category_encyclopedia_view()
        else:
            print("\nThank you for using our expert system")
            break