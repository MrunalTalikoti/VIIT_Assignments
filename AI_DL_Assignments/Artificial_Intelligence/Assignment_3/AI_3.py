facts = {
    "parent": [
        ("john", "mary"),
        ("john", "mike"),
        ("susan", "mary"),
        ("susan", "mike"),
        ("mary", "alice"),
        ("mike", "bob")
    ]
}

# Inference rules
def is_parent(x, y):
    return ("parent", (x, y)) in [("parent", f) for f in facts["parent"]]

def siblings(x, y):
    for p1 in facts["parent"]:
        for p2 in facts["parent"]:
            if p1[0] == p2[0] and p1[1] == x and p2[1] == y and x != y:
                return True
    return False

def grandparents(x, y):
    for (p, c) in facts["parent"]:
        if p == x:
            for (p2, c2) in facts["parent"]:
                if p2 == c and c2 == y:
                    return True
    return False

# Query parser
def query_family_tree(query):
    tokens = query.lower().split()
    
    if tokens[0] == "parents" and tokens[1] == "of":
        child = tokens[2]
        return [p for (p, c) in facts["parent"] if c == child]
    
    elif tokens[0] == "children" and tokens[1] == "of":
        parent = tokens[2]
        return [c for (p, c) in facts["parent"] if p == parent]
    
    elif tokens[0] == "siblings":
        x, y = tokens[2], tokens[4]
        return siblings(x, y)
    
    elif tokens[0] == "grandparent":
        x, y = tokens[2], tokens[4]
        return grandparents(x, y)
    
    else:
        return "Query not understood."

# ----------------- Example -----------------
if __name__ == "__main__":
    print("Family Tree Knowledge Base Parser")
    print("Examples: 'parents of mary', 'children of john', 'siblings mary and mike', 'grandparent john of alice'")

    while True:
        q = input("\nEnter query (or 'exit'): ")
        if q.lower() == "exit":
            break
        print("Answer:", query_family_tree(q))
explain the entire code step by step and alkso theorotically


