import random
import math

NUM_FINCTIONS = 20
MAX_DEPTH = 6
THRESHOLD = 500  

INPUT_SEED = 42          

PM_SUBTREE = 0.1
PM_POINT   = 0.20

class TreeNode:
    def __init__(self):
        self.child = []
        self.parent = None
        self.value = None

def protected_pow(a, b):
    if abs(b) > 5:
        b = 5 if b > 0 else -5
    try:
        if a < 0:
            if abs(b - round(b)) > 1e-9:
                return 1.0
            b = int(round(b))

        val = a ** b

        if isinstance(val, complex):
            return 1.0

        val = float(val)
        if abs(val) > 1e6:
            return 1e6 if val > 0 else -1e6
        return val
    except:
        return 1.0


def protected_sin(x):
    if isinstance(x, complex):
        return 0.0
    try:
        return math.sin(x)
    except:
        return 0.0


def protected_cos(x):
    if isinstance(x, complex):
        return 0.0
    try:
        return math.cos(x)
    except:
        return 0.0

def create_input():
    input_output = {}

    fixed = [0.0, 0.01, 0.1, 1.0,3.0 , 4.0, 5.0 , 11.0, 9.0, 3.0, 4.0, 6.0, 7.0, 8.0 , 9.5, 10.0 , -1.0 , -0.1 , -2.0 , -3.0 , -4.0 , -5.0 , -6.0]
    
    for x in fixed:
        
        y = x + 3 
        input_output[round(x, 6)] = float(y)

    while len(input_output) < 70:
        x = round(random.uniform(0, 10), 6)
        if x in input_output:
            continue
        y = x + 3 
        input_output[x] = float(y)

    return input_output


OPERATOR_COEFFICIENT = {
    "operator": ["*", "+", "-", "/", "pow", "sin", "cos"],
    "operand":  [0, 1, 2, 3, 4, 5, "x"]
}
NODE_KEY = ["operator", "operand"]

def create_trees():
    def create_tree(root, depth, max_depth):
        while depth < max_depth:
            if root.value[0] == "operator":
                if root.value[1] not in ("sin", "cos"):
                    first_child = TreeNode()
                    rand_node1 = random.randint(0, 1)
                    if rand_node1 == 0 and depth != max_depth - 1:
                        rand1 = random.randint(0, len(OPERATOR_COEFFICIENT["operator"]) - 1)
                    else:
                        rand_node1 = 1
                        rand1 = random.randint(0, len(OPERATOR_COEFFICIENT["operand"]) - 1)

                    second_child = TreeNode()
                    rand_node2 = random.randint(0, 1)
                    if rand_node2 == 0 and depth != max_depth - 1:
                        rand2 = random.randint(0, len(OPERATOR_COEFFICIENT["operator"]) - 1)
                    else:
                        rand_node2 = 1
                        rand2 = random.randint(0, len(OPERATOR_COEFFICIENT["operand"]) - 1)

                    first_child.value = [NODE_KEY[rand_node1], OPERATOR_COEFFICIENT[NODE_KEY[rand_node1]][rand1]]
                    second_child.value = [NODE_KEY[rand_node2], OPERATOR_COEFFICIENT[NODE_KEY[rand_node2]][rand2]]

                    child1 = create_tree(first_child, depth + 1, max_depth)
                    child2 = create_tree(second_child, depth + 1, max_depth)

                    child1.parent = root
                    child2.parent = root
                    root.child.append(child1)
                    root.child.append(child2)

                else:
                    first_child = TreeNode()
                    rand_node1 = random.randint(0, 1)
                    if rand_node1 == 0 and depth != max_depth - 1:
                        rand1 = random.randint(0, len(OPERATOR_COEFFICIENT["operator"]) - 1)
                    else:
                        rand_node1 = 1
                        rand1 = random.randint(0, len(OPERATOR_COEFFICIENT["operand"]) - 1)

                    first_child.value = [NODE_KEY[rand_node1], OPERATOR_COEFFICIENT[NODE_KEY[rand_node1]][rand1]]
                    child1 = create_tree(first_child, depth + 1, max_depth)

                    child1.parent = root
                    root.child.append(child1)

                return root
            else:
                return root

        return root

    functions = []
    for i in range(NUM_FINCTIONS):
        rand = random.randint(0, len(OPERATOR_COEFFICIENT["operator"]) - 1)
        root = TreeNode()
        root.value = ["operator", OPERATOR_COEFFICIENT["operator"][rand]]
        root = create_tree(root, 0, MAX_DEPTH)
        functions.append(root)
        print(f"{i}----------")
    return functions

def compute_fitness(functions, input_data):
    def compute_MSE(output, input_map):
        mse = 0.0
        for index, x in enumerate(input_map):
            mse += (output[index] - input_map[x]) ** 2
        return mse / len(input_map)

    def compute_fitnes(func, x):
        if len(func.child) == 0:
            return float(x) if func.value[1] == "x" else func.value[1]

        child_num = len(func.child)

        if child_num == 2:
            a = compute_fitnes(func.child[0], x)
            b = compute_fitnes(func.child[1], x)

            if func.value[1] == "*":
                return a * b
            elif func.value[1] == "+":
                return a + b
            elif func.value[1] == "-":
                return a - b
            elif func.value[1] == "/":
                if b == 0 or abs(b) < 1e-6:
                    return 1.0
                return a / b
            elif func.value[1] == "pow":
                return protected_pow(a, b)

        else:
            a = compute_fitnes(func.child[0], x)
            if func.value[1] == "sin":
                return protected_sin(a)
            elif func.value[1] == "cos":
                return protected_cos(a)

    mse_arr = []
    for f in functions:
        output = []
        for x in input_data:
            output.append(compute_fitnes(f, x))
        mse_arr.append(compute_MSE(output, input_data))

    return mse_arr


def print_tree(root):
    if root is None:
        return
    for c_n, c in enumerate(root.child):
        print(f"{root.value} childNumber {c_n} with value {c.value}")
        print_tree(c)


def tree_to_expr(node):
    if node is None:
        return "None"
    if len(node.child) == 0:
        v = node.value[1]
        return "x" if v == "x" else str(v)

    op = node.value[1]

    if op in ("sin", "cos"):
        return f"{op}({tree_to_expr(node.child[0])})"

    a = tree_to_expr(node.child[0])
    b = tree_to_expr(node.child[1])

    if op == "pow":
        return f"({a} ** {b})"
    if op == "+":
        return f"({a} + {b})"
    if op == "-":
        return f"({a} - {b})"
    if op == "*":
        return f"({a} * {b})"
    if op == "/":
        return f"({a} / {b})"

    return f"{op}({a},{b})"

def make_generation(functions, input_data, THRESHOLD):
    def clone_tree(node, parent=None):
        if node is None:
            return None
        new_node = TreeNode()
        new_node.value = node.value[:] if isinstance(node.value, list) else node.value
        new_node.parent = parent
        new_node.child = []
        for ch in node.child:
            new_child = clone_tree(ch, new_node)
            new_node.child.append(new_child)
        return new_node

    def count_nodes(t):
        if t is None:
            return 0
        return 1 + sum(count_nodes(ch) for ch in t.child)

    def tournament_pick(mse, k=3):
        best_i = None
        best_val = None
        for _ in range(k):
            i = random.randint(0, len(mse) - 1)
            if best_i is None or mse[i] < best_val:
                best_i = i
                best_val = mse[i]
        return best_i

    def build_parent_pool(mse, pool_size):
        return [tournament_pick(mse, k=3) for _ in range(pool_size)]

    def swap_subtrees(t1, t2, c1, c2):
        count = 0

        def dfs(t, target):
            nonlocal count
            if t is None:
                return None
            count += 1
            if count == target:
                return t
            for child in t.child:
                res = dfs(child, target)
                if res is not None:
                    return res
            return None

        count = 0
        n1 = dfs(t1, c1)
        count = 0
        n2 = dfs(t2, c2)

        if n1 is None or n2 is None:
            return t1, t2
        if n1.parent is None or n2.parent is None:
            return t1, t2

        p1, p2 = n1.parent, n2.parent
        i1 = p1.child.index(n1)
        i2 = p2.child.index(n2)

        p1.child[i1] = n2
        n2.parent = p1

        p2.child[i2] = n1
        n1.parent = p2

        return t1, t2

    def node_depth(n):
        d = 0
        while n is not None and n.parent is not None:
            d += 1
            n = n.parent
        return d

    def pick_random_nonroot(root):
        nodes = []
        def dfs(n):
            nodes.append(n)
            for ch in n.child:
                dfs(ch)
        dfs(root)
        if len(nodes) <= 1:
            return None
        return random.choice(nodes[1:])

    def gen_random_subtree(cur_depth, parent=None):
        node = TreeNode()
        node.parent = parent

        if cur_depth >= MAX_DEPTH:
            node.value = ["operand", random.choice(OPERATOR_COEFFICIENT["operand"])]
            return node

        choose_op = random.random() < 0.65
        if not choose_op:
            node.value = ["operand", random.choice(OPERATOR_COEFFICIENT["operand"])]
            return node

        op = random.choice(OPERATOR_COEFFICIENT["operator"])
        node.value = ["operator", op]

        if op in ("sin", "cos"):
            child = gen_random_subtree(cur_depth + 1, parent=node)
            node.child.append(child)
        else:
            c1 = gen_random_subtree(cur_depth + 1, parent=node)
            c2 = gen_random_subtree(cur_depth + 1, parent=node)
            node.child.append(c1)
            node.child.append(c2)

        return node

    def point_mutation(tree_root):
        n = pick_random_nonroot(tree_root)
        if n is None:
            return

        binary_ops = ["*", "+", "-", "/", "pow"]
        unary_ops = ["sin", "cos"]

        if n.value[0] == "operand":
            n.value = ["operand", random.choice(OPERATOR_COEFFICIENT["operand"])]
            return

        if len(n.child) == 1:
            n.value = ["operator", random.choice(unary_ops)]
        elif len(n.child) == 2:
            n.value = ["operator", random.choice(binary_ops)]

    def subtree_mutation(tree_root):
        n = pick_random_nonroot(tree_root)
        if n is None or n.parent is None:
            return

        p = n.parent
        idx = p.child.index(n)

        d = node_depth(n)
        if d >= MAX_DEPTH:
            point_mutation(tree_root)
            return

        new_sub = gen_random_subtree(d, parent=p)
        p.child[idx] = new_sub

    def mutation(tree_root):
        r = random.random()
        if r < PM_SUBTREE:
            subtree_mutation(tree_root)
        elif r < PM_SUBTREE + PM_POINT:
            point_mutation(tree_root)

    mse = compute_fitness(functions, input_data)
    best_mse_val = min(mse)
    best_idx = mse.index(best_mse_val)
    best_tree = clone_tree(functions[best_idx])

    gen = 0
    while gen < THRESHOLD and best_mse_val != 0:
        parent_pool = build_parent_pool(mse, pool_size=NUM_FINCTIONS)

        new_functions = []
        for _ in range(NUM_FINCTIONS // 2):
            p1_idx = random.choice(parent_pool)
            p2_idx = random.choice(parent_pool)

            t1 = clone_tree(functions[p1_idx])
            t2 = clone_tree(functions[p2_idx])

            n1 = count_nodes(t1)
            n2 = count_nodes(t2)
            min_n = min(n1, n2)
            

            if n1 >= 2 and n2 >= 2:
                c1 = random.randint(2, min_n)
                # c2 = random.randint(2, n2)
                t1, t2 = swap_subtrees(t1, t2, c1, c1)

            mutation(t1)
            mutation(t2)

            new_functions.append(t1)
            new_functions.append(t2)

        # elitism
        new_functions[-1] = clone_tree(best_tree)

        mse_new = compute_fitness(new_functions, input_data)

        gen_best_val = min(mse_new)
        gen_best_idx = mse_new.index(gen_best_val)
        if gen_best_val < best_mse_val:
            best_mse_val = gen_best_val
            best_tree = clone_tree(new_functions[gen_best_idx])

        functions = new_functions
        mse = mse_new
        gen += 1

    return functions, best_tree, best_mse_val

random.seed(INPUT_SEED)
input_data = create_input()
random.seed()

functions = create_trees()
_, best_tree, best_mse = make_generation(functions, input_data, THRESHOLD)

print_tree(best_tree)
print(f"Best MSE after {THRESHOLD} generations is {best_mse}")
print("Best expression found:", tree_to_expr(best_tree))
