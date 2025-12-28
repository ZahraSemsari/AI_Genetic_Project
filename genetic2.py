import random
import math
import matplotlib.pyplot as plt

NUM_FINCTIONS = 120
MAX_DEPTH = 5
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

def protected_sqrt(x):
    if isinstance(x, complex):
        return 0.0
    try:
        return math.sqrt(abs(x))
    except:
        return 0.0

def eval_tree(func, x):
    if len(func.child) == 0:
        return float(x) if func.value[1] == "x" else float(func.value[1])

    if len(func.child) == 2:
        a = eval_tree(func.child[0], x)
        b = eval_tree(func.child[1], x)

        op = func.value[1]
        if op == "*":
            return a * b
        if op == "+":
            return a + b
        if op == "-":
            return a - b
        if op == "/":
            if b == 0 or abs(b) < 1e-6:
                return 1.0
            return a / b
        if op == "pow":
            return protected_pow(a, b)

        return 1.0

    a = eval_tree(func.child[0], x)
    op = func.value[1]
    if op == "sin":
        return protected_sin(a)
    if op == "cos":
        return protected_cos(a)
    if op == "sqrt":
        return protected_sqrt(a)
    return 1.0

def target_func(x):
    return x * x + math.sin(3 * x) 

def create_input():
    input_output = {}
    fixed = [float(i) for i in range(-100, 101)]

    for x in fixed:
        y = target_func(x)
        input_output[round(x, 6)] = float(y)

    while len(input_output) < 1000:
        x = round(random.uniform(-100, 100), 6)
        if x in input_output:
            continue
        y = target_func(x)
        input_output[x] = float(y)

    return input_output

OPERATOR_COEFFICIENT = {
    "operator": ["*", "+", "-", "/", "pow", "sin", "cos", "sqrt"],
    "operand":  [0, 1, 2, 3, 4, 5, 0.1, 0.2, 0.3, "x"]
}
NODE_KEY = ["operator", "operand"]

def create_trees():
    unary_ops = ("sin", "cos", "sqrt")

    def pick_value(depth, max_depth):
        rand_node = random.randint(0, 1)
        if rand_node == 0 and depth != max_depth - 1:
            return ["operator", random.choice(OPERATOR_COEFFICIENT["operator"])]
        return ["operand", random.choice(OPERATOR_COEFFICIENT["operand"])]

    def create_tree(root, depth, max_depth):
        while depth < max_depth:
            if root.value[0] != "operator":
                return root

            if root.value[1] in unary_ops:
                child = TreeNode()
                child.value = pick_value(depth, max_depth)
                c1 = create_tree(child, depth + 1, max_depth)
                c1.parent = root
                root.child.append(c1)
                return root

            for _ in range(2):
                child = TreeNode()
                child.value = pick_value(depth, max_depth)
                c = create_tree(child, depth + 1, max_depth)
                c.parent = root
                root.child.append(c)
            return root

        return root

    functions = []
    for i in range(NUM_FINCTIONS):
        root = TreeNode()
        root.value = ["operator", random.choice(OPERATOR_COEFFICIENT["operator"])]
        functions.append(create_tree(root, 0, MAX_DEPTH))
    return functions

def tree_to_expr(node):
    if node is None:
        return "None"
    if len(node.child) == 0:
        v = node.value[1]
        return "x" if v == "x" else str(v)

    op = node.value[1]

    if op in ("sin", "cos", "sqrt"):
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
    unary_ops = ("sin", "cos", "sqrt")

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

    def tree_max_depth(root):
        def dfs(n, d):
            if n is None or len(n.child) == 0:
                return d
            return max(dfs(ch, d + 1) for ch in n.child)
        return dfs(root, 0)

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

        if op in unary_ops:
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
        unary_list = ["sin", "cos", "sqrt"]

        if n.value[0] == "operand":
            n.value = ["operand", random.choice(OPERATOR_COEFFICIENT["operand"])]
            return

        if len(n.child) == 1:
            n.value = ["operator", random.choice(unary_list)]
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

    items = list(input_data.items())
    n_items = len(items)

    def fitness_of_pop(pop):
        mse_arr = []
        for f in pop:
            mse = 0.0
            for x, y in items:
                d = eval_tree(f, x) - y
                mse += d * d
            mse_arr.append(mse / n_items)
        return mse_arr

    mse = fitness_of_pop(functions)
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

            if n1 >= 2 and n2 >= 2:
                t1_before = clone_tree(t1)
                t2_before = clone_tree(t2)

                c1 = random.randint(2, n1)
                c2 = random.randint(2, n2)

                t1, t2 = swap_subtrees(t1, t2, c1, c2)

                if tree_max_depth(t1) > MAX_DEPTH or tree_max_depth(t2) > MAX_DEPTH:
                    t1, t2 = t1_before, t2_before

            mutation(t1)
            mutation(t2)

            new_functions.append(t1)
            new_functions.append(t2)

        new_functions[-1] = clone_tree(best_tree)

        mse_new = fitness_of_pop(new_functions)

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

print(f"Best MSE after {THRESHOLD} generations is {best_mse}")
print("Best expression found:", tree_to_expr(best_tree))

xs_data = sorted(input_data.keys())
ys_data = [input_data[x] for x in xs_data]

xmin, xmax = xs_data[0], xs_data[-1]
n = 2000
xs = [xmin + (xmax - xmin) * i / n for i in range(n + 1)]

ys_true = [target_func(x) for x in xs]

y_scale = max(
    max(abs(v) for v in ys_data),
    max(abs(v) for v in ys_true)
)
y_cap = (y_scale * 1.1) + 1e-9

ys_pred = []
for x in xs:
    y = eval_tree(best_tree, x)
    if (not math.isfinite(y)) or abs(y) > y_cap:
        y = float("nan")
    ys_pred.append(y)

# fig, ax = plt.subplots(1, 2, figsize=(12, 4), sharey=True)


plt.figure(figsize=(10, 4))

plt.scatter(xs_data, ys_data, s=6, alpha=0.35, color="tab:gray", label="samples")
plt.plot(xs, ys_true, color="tab:orange", linewidth=2, label="true f(x)")
plt.plot(xs, ys_pred, color="tab:green", linewidth=2, label="GP best")

plt.title("True vs GP (overlay)")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("compare_overlay.png", dpi=300, bbox_inches="tight")
plt.show()


# ax[0].scatter(xs_data, ys_data, s=6, alpha=0.6, color="tab:blue", label="samples")
# ax[0].plot(xs, ys_true, color="tab:orange", linewidth=2, label="true f(x)")
# ax[0].set_title("Ground truth (data source)")
# ax[0].set_xlabel("x")
# ax[0].set_ylabel("y")
# ax[0].grid(True)
# ax[0].legend()

# ax[1].scatter(xs_data, ys_data, s=6, alpha=0.25, color="tab:gray", label="samples")
# ax[1].plot(xs, ys_pred, color="tab:green", linewidth=2, label="GP best")
# ax[1].set_title("GP output")
# ax[1].set_xlabel("x")
# ax[1].set_ylabel("y")
# ax[1].grid(True)
# ax[1].legend()

# plt.tight_layout()
# plt.savefig("compare_2plots.png", dpi=300, bbox_inches="tight")
# plt.show()


# err = []
# for x in xs:
#     yp = eval_tree(best_tree, x)
#     yt = target_func(x)
#     err.append(yp - yt)

# plt.figure(figsize=(10,3))
# plt.plot(xs, err)
# plt.title("Prediction error (GP - true)")
# plt.grid(True)
# plt.show()

