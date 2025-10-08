facts = ["A", "B"]

#(condition, conclusion)
rules = [
    (["A", "B"], "C"),  # If A and B are true, then C is true
    (["C"], "D"),       # If C is true, then D is true
    (["D"], "E")        # If D is true, then E is true
]

def forward_chaining(facts, rules):
    inferred = set(facts) 
    new_fact_added = True

    while new_fact_added:
        new_fact_added = False  
        for rule in rules:  
            conditions, conclusion = rule  
            
            # Check if all conditions are satisfied
            all_conditions_met = True
            for condition in conditions: 
                if condition not in inferred:
                    all_conditions_met = False
                    break  
            
     
            if all_conditions_met and conclusion not in inferred:
                inferred.add(conclusion)  
                print(f"Inferred new fact: {conclusion}")
                new_fact_added = True  
                
    return inferred  


print("Initial facts:", facts)
inferred_facts = forward_chaining(facts, rules)
print("Final inferred facts:", inferred_facts)
