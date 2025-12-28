import random
import copy
import math
random.seed(42)

NUM_POPULATION = 100

class TreeNode():
    def __init__(self):
        self.child = []
        self.parent = None
        self.value = None


def clone_tree(node):
    new_node = TreeNode()
    new_node.value = node.value[:] if isinstance(node.value, list) else node.value
    new_node.child = [clone_tree(c) for c in node.child]
    new_node.parent = None  # عمداً کپی نمی‌کنیم
    return new_node



def protected_pow(a, b):
    if abs(b) > 5:
        b = 5
    try:
        val = a ** b
        if isinstance(val, complex):
            return float(val.real) 
        
        if abs(val) > 1e6:
            return 1e6
        return float(val)
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
    for _ in range(80):
        x = random.uniform(0, 10)
        while x in input_output:           # یکتا
            x = random.uniform(0, 10)
        y = x * x + 2 * x + 1
        input_output[x] = float(y)
    print(input_output)
    return input_output

# print(create_input())


OPERATOR_COEFFICIENT = { 'operator' : ['*' , '+' , '-' , '/' , 'pow' , 'sin' , 'cos'] , 'operand' : [1 ,2 ,3 ,4 ,5 ,'x'] }
NODE_KEY = ['operator' , 'operand']

def create_trees() :
    def print_tree(root) :
        if root == None :
            return
        for c_n , c in enumerate(root.child) : 
            print(f"{root.value} childNumber {c_n} with value {c.value}") 
            print_tree(c)
        


    def create_tree(root, depth , max_depth) :
        while(depth < max_depth) :
            if root.value[0] == 'operator' :
                if root.value[1] != 'sin' and root.value[1] != 'cos':
                    first_child = TreeNode()
                    rand_node1 = random.randint(0,1)
                    if rand_node1 == 0 and depth != max_depth-1:
                        rand1 = random.randint(0,len(OPERATOR_COEFFICIENT['operator']) -1) 
                    else: 
                        rand_node1 = 1
                        rand1 = random.randint(0,len(OPERATOR_COEFFICIENT['operand']) -1)


                    second_child = TreeNode()
                    rand_node2 = random.randint(0,1)
                    if rand_node2 == 0 and depth != max_depth-1:
                        rand2 = random.randint(0,len(OPERATOR_COEFFICIENT['operator'])-1) 
                    else : 
                        rand_node2 = 1
                        rand2 = random.randint(0,len(OPERATOR_COEFFICIENT['operand'])-1)

                    first_child.value = [NODE_KEY[rand_node1] , OPERATOR_COEFFICIENT[NODE_KEY[rand_node1]][rand1]]
                    second_child.value = [NODE_KEY[rand_node2] , OPERATOR_COEFFICIENT[NODE_KEY[rand_node2]][rand2]]
                    child1 = create_tree(first_child , depth + 1 , max_depth)
                    child2 = create_tree(second_child , depth + 1 , max_depth)
                    root.child.append(child1)
                    root.child.append(child2)
                
                else :
                    first_child = TreeNode()
                    rand_node1 = random.randint(0,1)
                    if rand_node1 == 0 and depth != max_depth-1:
                        rand1 = random.randint(0,len(OPERATOR_COEFFICIENT['operator']) -1) 
                    else : 
                        rand_node1 = 1
                        rand1 = random.randint(0,len(OPERATOR_COEFFICIENT['operand']) -1)

                    first_child.value = [NODE_KEY[rand_node1] , OPERATOR_COEFFICIENT[NODE_KEY[rand_node1]][rand1]]
                    child1 = create_tree(first_child , depth + 1 , max_depth)
                    root.child.append(child1)
                return root
            else :
                return root
        return root 


    max_depth = 5
    depth = 0
    functions = []
    for i in range(NUM_POPULATION):
        rand = random.randint(0,6) 
        root = TreeNode()
        root.value = ['operator',OPERATOR_COEFFICIENT['operator'][rand]]
        root = create_tree(root , depth , max_depth)
        functions.append(root)
    
        # print_tree(root)
        # print(f"{i}----------")
    return functions


# create_trees()            


dataset = create_input()    
def compute_fitness(functions) :
        
    def compute_MSE(output , input) :
        mse = 0
        for index,i in enumerate(input) :
            mse += (output[index] - input[i]) ** 2
        MSE = mse / len(input)
        return MSE 

    def compute_fitnes(func , input) : 
        if len(func.child) == 0 :
            if func.value[1] == 'x' :
                return float(input)
            else :
                return func.value[1] 
        
        child_num = len(func.child)

        if child_num == 2 :
            first_opernad = compute_fitnes(func.child[0] , input)
            second_operand = compute_fitnes(func.child[1] , input)
            if func.value[1] == '*' :
                return first_opernad * second_operand
            elif func.value[1] == '+' :
                return first_opernad + second_operand            
            elif func.value[1] == '-' :
                return first_opernad - second_operand            
            elif func.value[1] == '/' :
                if second_operand == 0 :
                    return 1.0
                if abs(second_operand) < 1e-6:
                    return 1.0
                return first_opernad / second_operand            
            elif func.value[1] == 'pow':
                return protected_pow(first_opernad, second_operand)
            
        else :
            first_opernad = compute_fitnes(func.child[0] , input)
            if func.value[1] == 'sin' :
                return protected_sin(first_opernad)
            elif func.value[1] == 'cos' :
                return protected_cos(first_opernad)




    # functions = create_trees()
    
    output = []
    mse_arr = []

    for f in functions :
        for i in dataset:
            output.append(compute_fitnes(f , i))
        # print(output)
        mse = compute_MSE(output , dataset)
        mse_arr.append(mse)
        output = []
    # print(mse_arr)
    return (mse_arr , dataset )


# compute_fitness(functions)


def make_generation(functions):

    threshold = 300
    TOURNAMENT_K = 3
    ELITE = 1  # همیشه بهترین رو نگه دار

    def count_nodes(t):
        total = 1
        for c in t.child:
            total += count_nodes(c)
        return total

    # ✅ فشار علیه bloat (کوچیک نگه داشتن درخت)
    # اگر دیدی زیادی سخت می‌گیره، ALPHA رو کوچیک‌تر کن
    ALPHA = 0.001

    def penalized_fitness(mse_list, funcs):
        # fitness = mse + alpha * size
        return [mse_list[i] + ALPHA * count_nodes(funcs[i]) for i in range(len(funcs))]

    def tournament_select(fitness_list):
        best_i = None
        best_val = float("inf")
        for _ in range(TOURNAMENT_K):
            i = random.randint(0, len(fitness_list) - 1)
            if fitness_list[i] < best_val:
                best_val = fitness_list[i]
                best_i = i
        return best_i

    # --- اول fitness نسل اولیه ---
    mse, _ = compute_fitness(functions)
    fit = penalized_fitness(mse, functions)

    for gen in range(threshold):

        # ✅ بهترین فرد واقعی (برای elitism)
        best_idx = min(range(len(fit)), key=lambda i: fit[i])
        best_individual = clone_tree(functions[best_idx])
        best_score = fit[best_idx]

        # --- selection: ساخت نسل جدید فقط با انتخاب ---
        new_functions = []
        for _ in range(NUM_POPULATION):
            p = tournament_select(fit)
            new_functions.append(clone_tree(functions[p]))

        # ✅ حالا crossover/mutation رو روی offspring انجام بده (نه روی نسل قبلی!)
        # همون تابعی که خودت ساختی:
        #   crossover_mutation(new_functions)
        # (این تابع داخلش هم crossover داره هم mutation)
        def crossover_mutation(functions):

            MUT_RATE = 0.25
            MAX_MUT_DEPTH = 3

            def trees_equal(t1, t2):
                if t1.value != t2.value:
                    return False
                if len(t1.child) != len(t2.child):
                    return False
                for c1, c2 in zip(t1.child, t2.child):
                    if not trees_equal(c1, c2):
                        return False
                return True

            def count_nodes_local(t):
                total = 1
                for c in t.child:
                    total += count_nodes_local(c)
                return total

            def find_node_with_parent(root, target_index):
                counter = -1
                result = None

                def dfs(node, parent, child_idx):
                    nonlocal counter, result
                    if result is not None:
                        return
                    counter += 1
                    if counter == target_index:
                        result = (node, parent, child_idx)
                        return
                    for i, c in enumerate(node.child):
                        dfs(c, node, i)

                dfs(root, None, None)
                return result

            def is_in_subtree(root, target):
                if root is target:
                    return True
                for c in root.child:
                    if is_in_subtree(c, target):
                        return True
                return False

            def swap_subtrees(t1, t2, idx1, idx2):
                res1 = find_node_with_parent(t1, idx1)
                res2 = find_node_with_parent(t2, idx2)
                if res1 is None or res2 is None:
                    return

                n1, p1, i1 = res1
                n2, p2, i2 = res2

                if p1 is None or p2 is None:
                    return

                if is_in_subtree(n1, p2) or is_in_subtree(n2, p1):
                    return

                sub1 = clone_tree(n1)
                sub2 = clone_tree(n2)

                p1.child[i1] = sub2
                p2.child[i2] = sub1

            def random_subtree(depth=0):
                n = TreeNode()
                if depth >= MAX_MUT_DEPTH:
                    n.value = ['operand', random.choice(OPERATOR_COEFFICIENT['operand'])]
                    return n

                if random.random() < 0.7:
                    op = random.choice(OPERATOR_COEFFICIENT['operator'])
                    n.value = ['operator', op]
                    if op in ('sin', 'cos'):
                        n.child = [random_subtree(depth + 1)]
                    else:
                        n.child = [random_subtree(depth + 1), random_subtree(depth + 1)]
                else:
                    n.value = ['operand', random.choice(OPERATOR_COEFFICIENT['operand'])]
                return n

            def mutate_tree(t):
                n = count_nodes_local(t)
                if n <= 1:
                    return
                idx = random.randint(1, n - 1)
                res = find_node_with_parent(t, idx)
                if res is None:
                    return
                node, parent, child_idx = res
                if parent is None:
                    return
                parent.child[child_idx] = random_subtree(0)

            # crossover روی کل offspring
            j = 0
            while j < len(functions):
                r1 = random.randint(0, len(functions) - 1)
                r2 = random.randint(0, len(functions) - 1)
                t1 = functions[r1]
                t2 = functions[r2]

                attempts = 0
                while trees_equal(t1, t2):
                    r2 = random.randint(0, len(functions) - 1)
                    t2 = functions[r2]
                    attempts += 1
                    if attempts > 50:
                        break

                if trees_equal(t1, t2):
                    j += 1
                    continue

                n1 = count_nodes_local(t1)
                n2 = count_nodes_local(t2)
                if n1 <= 1 or n2 <= 1:
                    j += 1
                    continue

                idx1 = random.randint(1, n1 - 1)
                idx2 = random.randint(1, n2 - 1)
                swap_subtrees(t1, t2, idx1, idx2)

                j += 1

            # mutation بعد از crossover
            for t in functions:
                if random.random() < MUT_RATE:
                    mutate_tree(t)

        crossover_mutation(new_functions)

        # --- elitism صحیح: بدترینِ new_functions رو با best_individual جایگزین کن ---
        if ELITE == 1:
            new_mse, _ = compute_fitness(new_functions)
            new_fit = [new_mse[i] + ALPHA * count_nodes(new_functions[i]) for i in range(len(new_functions))]

            worst_pos = max(range(len(new_fit)), key=lambda i: new_fit[i])
            new_functions[worst_pos] = best_individual
        else:
            new_mse, _ = compute_fitness(new_functions)
            new_fit = [new_mse[i] + ALPHA * count_nodes(new_functions[i]) for i in range(len(new_functions))]

        # نسل بعد
        functions = new_functions
        mse = new_mse
        fit = new_fit

    # خروجی بهترین
    best_idx = min(range(len(fit)), key=lambda i: fit[i])
    final_mse, _ = compute_fitness(functions)
    print(f"Final Best MSE: {min(final_mse)}")
    return functions[best_idx]


def display_tree_limited(root, max_depth=6, indent="", depth=0):
    if root is None:
        return
    print(f"{indent}{root.value}")
    if depth >= max_depth:
        print(f"{indent}  ...")
        return
    for child in root.child:
        display_tree_limited(child, max_depth, indent + "  ", depth + 1)

# استفاده:


# 2. Run the evolution
functions = create_trees()
best_function_tree = make_generation(functions)

# 3. See the answer
print("\n--- THE WINNING FORMULA ---")
display_tree_limited(best_function_tree, max_depth=6)









# ######################################################################################3



import random
import math
random.seed(42)

NUM_FINCTIONS = 100

class TreeNode():
    def __init__(self):
        self.child = []
        self.parent = None
        self.value = None


def protected_pow(a, b):
    # محدود کردن توان
    if abs(b) > 5:
        b = 5 if b > 0 else -5

    try:
        # اگر پایه منفی و توان عدد صحیح نیست → complex می‌دهد
        if a < 0:
            # چک "تقریباً صحیح بودن"
            if abs(b - round(b)) > 1e-9:
                return 1.0
            b = int(round(b))

        val = a ** b

        # اگر به هر دلیلی complex شد
        if isinstance(val, complex):
            return 1.0

        val = float(val)

        # کلیپ کردن مقدارهای خیلی بزرگ
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


# def create_input() :
#     input_output = dict()
#     input = 0
#     for _ in range(0,45) :
#         i = random.uniform(0, 10)
#         for k in input_output :
#             if k == i :
#                 while k == i :
#                     i = random.uniform(0, 10)
#             else :
#                 input = i

#         output = input * input + 2 * input + 1
#         input_output[input] = float(output) 
#     print(input_output)
#     return input_output


def create_input():
    input_output = {}
    while len(input_output) < 80:
        x = round(random.uniform(0, 10), 6)  # 6 رقم اعشار → امکان تکرار قابل کنترل
        if x in input_output:
            continue
        y = x * x + 2 * x + 1
        input_output[x] = float(y)
    return input_output



# print(create_input())


OPERATOR_COEFFICIENT = { 'operator' : ['*' , '+' , '-' , '/' , 'pow' , 'sin' , 'cos'] , 'operand' : [1 ,2 ,3 ,4 ,5 ,'x'] }
NODE_KEY = ['operator' , 'operand']

def print_tree(root) :
    if root == None :
        return
    for c_n , c in enumerate(root.child) : 
        print(f"{root.value} childNumber {c_n} with value {c.value}") 
        print_tree(c)

def create_trees() :
        


    def create_tree(root, depth , max_depth) :
        while(depth < max_depth) :
            if root.value[0] == 'operator' :
                if root.value[1] != 'sin' and root.value[1] != 'cos':
                    first_child = TreeNode()
                    rand_node1 = random.randint(0,1)
                    if rand_node1 == 0 and depth != max_depth-1:
                        rand1 = random.randint(0,len(OPERATOR_COEFFICIENT['operator']) -1) 
                    else: 
                        rand_node1 = 1
                        rand1 = random.randint(0,len(OPERATOR_COEFFICIENT['operand']) -1)


                    second_child = TreeNode()
                    rand_node2 = random.randint(0,1)
                    if rand_node2 == 0 and depth != max_depth-1:
                        rand2 = random.randint(0,len(OPERATOR_COEFFICIENT['operator'])-1) 
                    else : 
                        rand_node2 = 1
                        rand2 = random.randint(0,len(OPERATOR_COEFFICIENT['operand'])-1)

                    first_child.value = [NODE_KEY[rand_node1] , OPERATOR_COEFFICIENT[NODE_KEY[rand_node1]][rand1]]
                    second_child.value = [NODE_KEY[rand_node2] , OPERATOR_COEFFICIENT[NODE_KEY[rand_node2]][rand2]]
                    child1 = create_tree(first_child , depth + 1 , max_depth)
                    child2 = create_tree(second_child , depth + 1 , max_depth)
                    child1.parent = root
                    child2.parent = root
                    root.child.append(child1)
                    root.child.append(child2)
                
                else :
                    first_child = TreeNode()
                    rand_node1 = random.randint(0,1)
                    if rand_node1 == 0 and depth != max_depth-1:
                        rand1 = random.randint(0,len(OPERATOR_COEFFICIENT['operator']) -1) 
                    else : 
                        rand_node1 = 1
                        rand1 = random.randint(0,len(OPERATOR_COEFFICIENT['operand']) -1)

                    first_child.value = [NODE_KEY[rand_node1] , OPERATOR_COEFFICIENT[NODE_KEY[rand_node1]][rand1]]
                    child1 = create_tree(first_child , depth + 1 , max_depth)
                    child1.parent = root
                    root.child.append(child1)
                return root
            else :
                return root
        return root 


    max_depth = 5
    depth = 0
    functions = []
    for i in range(NUM_FINCTIONS):
        rand = random.randint(0,6) 
        root = TreeNode()
        root.value = ['operator',OPERATOR_COEFFICIENT['operator'][rand]]
        root = create_tree(root , depth , max_depth)
        functions.append(root)
    
        print_tree(root)
        print(f"{i}----------")
    return functions


# create_trees()            


input = create_input()    
def compute_fitness(functions) :
        
    def compute_MSE(output , input) :
        mse = 0
        for index,i in enumerate(input) :
            mse += (output[index] - input[i]) ** 2
        MSE = mse / len(input)
        return MSE 

    def compute_fitnes(func , input) : 
        if len(func.child) == 0 :
            if func.value[1] == 'x' :
                return float(input)
            else :
                return func.value[1] 
        
        child_num = len(func.child)

        if child_num == 2 :
            first_opernad = compute_fitnes(func.child[0] , input)
            second_operand = compute_fitnes(func.child[1] , input)
            if func.value[1] == '*' :
                return first_opernad * second_operand
            elif func.value[1] == '+' :
                return first_opernad + second_operand            
            elif func.value[1] == '-' :
                return first_opernad - second_operand            
            elif func.value[1] == '/' :
                if second_operand == 0 :
                    return 1.0
                if abs(second_operand) < 1e-6:
                    return 1.0
                return first_opernad / second_operand            
            elif func.value[1] == 'pow':
                return protected_pow(first_opernad, second_operand)
            
        else :
            first_opernad = compute_fitnes(func.child[0] , input)
            if func.value[1] == 'sin' :
                return protected_sin(first_opernad)
            elif func.value[1] == 'cos' :
                return protected_cos(first_opernad)




    # functions = create_trees()
    
    output = []
    mse_arr = []

    for f in functions :
        for i in input:
            output.append(compute_fitnes(f , i))
        # print(output)
        mse = compute_MSE(output , input)
        mse_arr.append(mse)
        output = []
    print(mse_arr)
    return (mse_arr , input )


# compute_fitness(functions)




def make_generation(functions) :
    def choose_best_node(mse , input_output) :
        mse_len = len(mse)
        best_choise = []

        for _ in range(NUM_FINCTIONS) :
            choise = []
            for _ in range(3) : 
                i = random.randint(0, mse_len-1)
                choise.append((i , mse[i]))
            best_choise.append(min(choise , key=lambda x:x[1]))

        return best_choise

    def crossover_mutation(functions) :
        def clone_tree(node, parent=None):
            if node is None:
                return None
            new_node = TreeNode()
            # اگر value لیست است، کپی کن
            new_node.value = node.value[:] if isinstance(node.value, list) else node.value
            new_node.parent = parent
            new_node.child = []
            for ch in node.child:
                new_child = clone_tree(ch, new_node)
                new_node.child.append(new_child)
            return new_node


        def trees_equal(t1, t2):
            if t1.value != t2.value:
                return False
            if len(t1.child) != len(t2.child):
                return False
            for c1, c2 in zip(t1.child, t2.child):
                if not trees_equal(c1, c2):
                    return False
            return True


        def find_child(t1) :
            counter = 1
            for c in t1.child :
                counter += find_child(c)
            return counter 
        
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
            child_t1 = dfs(t1, c1)

            count = 0
            child_t2 = dfs(t2, c2)

            if child_t1 is None or child_t2 is None:
                return t1, t2

            if child_t1.parent is None or child_t2.parent is None:
                return t1, t2

            p1 = child_t1.parent
            p2 = child_t2.parent

            i1 = p1.child.index(child_t1)
            i2 = p2.child.index(child_t2)

            p1.child[i1] = child_t2
            child_t2.parent = p1

            p2.child[i2] = child_t1
            child_t1.parent = p2

            return t1, t2



        j = 0
        new_functions = []
        while j < NUM_FINCTIONS//2 : 
            r1 = random.randint(0,len(functions)-1)
            r2 = random.randint(0,len(functions)-1)

            t1 = clone_tree(functions[r1])
            t2 = clone_tree(functions[r2])

            attempts = 0
            while trees_equal(t1, t2) and attempts < NUM_FINCTIONS:
                r2 = random.randint(0, len(functions) - 1)
                t2 = clone_tree(functions[r2])
                attempts += 1


            c1_num = find_child(t1)
            c2_num = find_child(t2)

            c1 = random.randint(2 , c1_num )
            c2 = random.randint(2 , c2_num )

            t1, t2 = swap_subtrees(t1, t2, c1, c2)
            new_functions.append(t1)
            new_functions.append(t2)
            j+=1

        return new_functions
            


    threshold = 400
    j = 0
    (mse , input_output) = compute_fitness(functions)
    b_mse = min(mse)
    b_index = mse.index(b_mse)
    best_mse = (b_index , b_mse)
    changed = 0



    while j < threshold and best_mse[1] != 0 :  
        changed = 0
        new_functions = crossover_mutation(functions)
        (mse , input_output) = compute_fitness(new_functions)
        best_nodes = choose_best_node(mse , input_output)

        best_temp = min(best_nodes , key=lambda x:x[1])
        if best_temp[1] < best_mse[1]:
            best_mse = best_temp        
            changed = 1

        if changed == 0:
            new_functions[len(new_functions)-1] = functions[best_mse[0]]

        functions = new_functions
        j += 1
    
    if best_mse[1] == 0 :
        print_tree(functions[best_mse[0]])
        print("Found exact solution with MSE = 0")
    else :
        print_tree(functions[best_mse[0]])
        print(f"Best MSE after {threshold} generations is {best_mse[1]} at index {best_mse[0]}")

functions = create_trees()
make_generation(functions)



#######################################################################################


import random
import math
random.seed(42)

NUM_FINCTIONS = 100

class TreeNode():
    def __init__(self):
        self.child = []
        self.parent = None
        self.value = None


def protected_pow(a, b):
    # محدود کردن توان
    if abs(b) > 5:
        b = 5 if b > 0 else -5

    try:
        # اگر پایه منفی و توان عدد صحیح نیست → complex می‌دهد
        if a < 0:
            # چک "تقریباً صحیح بودن"
            if abs(b - round(b)) > 1e-9:
                return 1.0
            b = int(round(b))

        val = a ** b

        # اگر به هر دلیلی complex شد
        if isinstance(val, complex):
            return 1.0

        val = float(val)

        # کلیپ کردن مقدارهای خیلی بزرگ
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


# def create_input() :
#     input_output = dict()
#     input = 0
#     for _ in range(0,45) :
#         i = random.uniform(0, 10)
#         for k in input_output :
#             if k == i :
#                 while k == i :
#                     i = random.uniform(0, 10)
#             else :
#                 input = i

#         output = input * input + 2 * input + 1
#         input_output[input] = float(output) 
#     print(input_output)
#     return input_output


def create_input():
    input_output = {}
    while len(input_output) < 80:
        x = round(random.uniform(0, 10), 6)  # 6 رقم اعشار → امکان تکرار قابل کنترل
        if x in input_output:
            continue
        y = x * x + 2 * x + 1
        input_output[x] = float(y)
    return input_output



# print(create_input())


OPERATOR_COEFFICIENT = { 'operator' : ['*' , '+' , '-' , '/' , 'pow' , 'sin' , 'cos'] , 'operand' : [1 ,2 ,3 ,4 ,5 ,'x'] }
NODE_KEY = ['operator' , 'operand']

def print_tree(root) :
    if root == None :
        return
    for c_n , c in enumerate(root.child) : 
        print(f"{root.value} childNumber {c_n} with value {c.value}") 
        print_tree(c)

def create_trees() :
        


    def create_tree(root, depth , max_depth) :
        while(depth < max_depth) :
            if root.value[0] == 'operator' :
                if root.value[1] != 'sin' and root.value[1] != 'cos':
                    first_child = TreeNode()
                    rand_node1 = random.randint(0,1)
                    if rand_node1 == 0 and depth != max_depth-1:
                        rand1 = random.randint(0,len(OPERATOR_COEFFICIENT['operator']) -1) 
                    else: 
                        rand_node1 = 1
                        rand1 = random.randint(0,len(OPERATOR_COEFFICIENT['operand']) -1)


                    second_child = TreeNode()
                    rand_node2 = random.randint(0,1)
                    if rand_node2 == 0 and depth != max_depth-1:
                        rand2 = random.randint(0,len(OPERATOR_COEFFICIENT['operator'])-1) 
                    else : 
                        rand_node2 = 1
                        rand2 = random.randint(0,len(OPERATOR_COEFFICIENT['operand'])-1)

                    first_child.value = [NODE_KEY[rand_node1] , OPERATOR_COEFFICIENT[NODE_KEY[rand_node1]][rand1]]
                    second_child.value = [NODE_KEY[rand_node2] , OPERATOR_COEFFICIENT[NODE_KEY[rand_node2]][rand2]]
                    child1 = create_tree(first_child , depth + 1 , max_depth)
                    child2 = create_tree(second_child , depth + 1 , max_depth)
                    child1.parent = root
                    child2.parent = root
                    root.child.append(child1)
                    root.child.append(child2)
                
                else :
                    first_child = TreeNode()
                    rand_node1 = random.randint(0,1)
                    if rand_node1 == 0 and depth != max_depth-1:
                        rand1 = random.randint(0,len(OPERATOR_COEFFICIENT['operator']) -1) 
                    else : 
                        rand_node1 = 1
                        rand1 = random.randint(0,len(OPERATOR_COEFFICIENT['operand']) -1)

                    first_child.value = [NODE_KEY[rand_node1] , OPERATOR_COEFFICIENT[NODE_KEY[rand_node1]][rand1]]
                    child1 = create_tree(first_child , depth + 1 , max_depth)
                    child1.parent = root
                    root.child.append(child1)
                return root
            else :
                return root
        return root 


    max_depth = 5
    depth = 0
    functions = []
    for i in range(NUM_FINCTIONS):
        rand = random.randint(0,6) 
        root = TreeNode()
        root.value = ['operator',OPERATOR_COEFFICIENT['operator'][rand]]
        root = create_tree(root , depth , max_depth)
        functions.append(root)
    
        print_tree(root)
        print(f"{i}----------")
    return functions


# create_trees()            


input = create_input()    
def compute_fitness(functions) :
        
    def compute_MSE(output , input) :
        mse = 0
        for index,i in enumerate(input) :
            mse += (output[index] - input[i]) ** 2
        MSE = mse / len(input)
        return MSE 

    def compute_fitnes(func , input) : 
        if len(func.child) == 0 :
            if func.value[1] == 'x' :
                return float(input)
            else :
                return func.value[1] 
        
        child_num = len(func.child)

        if child_num == 2 :
            first_opernad = compute_fitnes(func.child[0] , input)
            second_operand = compute_fitnes(func.child[1] , input)
            if func.value[1] == '*' :
                return first_opernad * second_operand
            elif func.value[1] == '+' :
                return first_opernad + second_operand            
            elif func.value[1] == '-' :
                return first_opernad - second_operand            
            elif func.value[1] == '/' :
                if second_operand == 0 :
                    return 1.0
                if abs(second_operand) < 1e-6:
                    return 1.0
                return first_opernad / second_operand            
            elif func.value[1] == 'pow':
                return protected_pow(first_opernad, second_operand)
            
        else :
            first_opernad = compute_fitnes(func.child[0] , input)
            if func.value[1] == 'sin' :
                return protected_sin(first_opernad)
            elif func.value[1] == 'cos' :
                return protected_cos(first_opernad)




    # functions = create_trees()
    
    output = []
    mse_arr = []

    for f in functions :
        for i in input:
            output.append(compute_fitnes(f , i))
        # print(output)
        mse = compute_MSE(output , input)
        mse_arr.append(mse)
        output = []
    print(mse_arr)
    return (mse_arr , input )


# compute_fitness(functions)



def make_generation(functions):
    # ---------- helpers ----------
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
        total = 1
        for ch in t.child:
            total += count_nodes(ch)
        return total

    def tournament_pick(mse, k=3):
        # یک برنده تورنمنت k-تایی برمی‌گرداند (ایندکس)
        best_i = None
        best_val = None
        for _ in range(k):
            i = random.randint(0, len(mse) - 1)
            if best_i is None or mse[i] < best_val:
                best_i = i
                best_val = mse[i]
        return best_i

    def build_parent_pool(mse, pool_size):
        # pool_size تا ایندکس خوب می‌سازیم
        return [tournament_pick(mse, k=3) for _ in range(pool_size)]

    def swap_subtrees(t1, t2, c1, c2):
        # n-اُمین نود preorder (ریشه هم شمرده می‌شود)
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
        # طبق فرض تو: ریشه انتخاب نمی‌شود، ولی برای اطمینان:
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

    # ---------- GA loop ----------
    threshold = 400

    mse, _ = compute_fitness(functions)
    best_mse_val = min(mse)
    best_idx = mse.index(best_mse_val)
    best_tree = clone_tree(functions[best_idx])  # ✅ بهترین درخت را خودِ آبجکت نگه می‌داریم

    gen = 0
    while gen < threshold and best_mse_val != 0:
        # 1) parent pool از روی fitness نسل فعلی
        parent_pool = build_parent_pool(mse, pool_size=NUM_FINCTIONS)

        # 2) تولید نسل جدید با crossover (والدها از pool)
        new_functions = []
        for _ in range(NUM_FINCTIONS // 2):
            p1_idx = random.choice(parent_pool)
            p2_idx = random.choice(parent_pool)
            # اگر خواستی می‌تونی اینجا جلوگیری از برابر بودن بذاری، ولی ضروری نیست.

            t1 = clone_tree(functions[p1_idx])
            t2 = clone_tree(functions[p2_idx])

            n1 = count_nodes(t1)
            n2 = count_nodes(t2)

            # اگر درخت خیلی کوچک بود، فقط همون کپی‌ها رو اضافه کن
            if n1 < 2 or n2 < 2:
                new_functions.append(t1)
                new_functions.append(t2)
                continue

            # چون نمی‌خوای ریشه انتخاب شه: از 2 تا n
            c1 = random.randint(2, n1)
            c2 = random.randint(2, n2)

            t1, t2 = swap_subtrees(t1, t2, c1, c2)
            new_functions.append(t1)
            new_functions.append(t2)

        # 3) Elitism درست: بهترینِ کل تا این لحظه رو وارد نسل جدید کن
        new_functions[-1] = clone_tree(best_tree)

        # 4) fitness نسل جدید
        mse_new, _ = compute_fitness(new_functions)

        # 5) آپدیت بهترینِ کل
        gen_best_val = min(mse_new)
        gen_best_idx = mse_new.index(gen_best_val)
        if gen_best_val < best_mse_val:
            best_mse_val = gen_best_val
            best_tree = clone_tree(new_functions[gen_best_idx])

        # 6) حرکت به نسل بعد
        functions = new_functions
        mse = mse_new
        gen += 1

    # ---------- report ----------
    print_tree(best_tree)
    if best_mse_val == 0:
        print("Found exact solution with MSE = 0")
    else:
        print(f"Best MSE after {threshold} generations is {best_mse_val}")

    return functions, best_tree, best_mse_val

functions = create_trees()
make_generation(functions)




















####################################################################33


import random
import math

# ----------------- تنظیمات -----------------
NUM_FINCTIONS = 10
MAX_DEPTH = 5
THRESHOLD = 400  # تعداد نسل‌ها

# برای اینکه دیتاست ثابت بماند ولی تکامل را بتوانی با seed های مختلف امتحان کنی:
INPUT_SEED = 42          # دیتاست
EVOLUTION_SEED = 42      # تکامل (اگر None بگذاری هر بار فرق می‌کند)

# نرخ‌های mutation (همه جا یکسان استفاده می‌شوند)
PM_SUBTREE = 0.05
PM_POINT   = 0.20


class TreeNode:
    def __init__(self):
        self.child = []
        self.parent = None
        self.value = None


# ----------------- توابع محافظتی -----------------
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


# ----------------- دیتا -----------------
def create_input():
    input_output = {}

    # نقاط “سخت” که جلوی تقلب‌هایی مثل x^(0.01) را می‌گیرند
    # fixed = [0.0, 0.001, 0.01, 0.1, 1.0, 10.0]
    fixed = [0.0, 0.01, 0.1, 1.0, 5.0 , 11.0, 9.0, 3.0, 4.0, 6.0, 7.0, 8.0]
    
    for x in fixed:
        
        y = x*x + math.cos(x) 
        input_output[round(x, 6)] = float(y)

    while len(input_output) < 60:
        x = round(random.uniform(0, 10), 6)
        if x in input_output:
            continue
        y = x*x + math.cos(x) 
        input_output[x] = float(y)

    return input_output


OPERATOR_COEFFICIENT = {
    "operator": ["*", "+", "-", "/", "pow", "sin", "cos"],
    "operand":  [0, 1, 2, 3, 4, 5, "x"]
}
NODE_KEY = ["operator", "operand"]


# ----------------- ساخت درخت‌ها -----------------
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


# ----------------- Fitness -----------------
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


# ----------------- چاپ و تبدیل به عبارت -----------------
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


# ----------------- GA (همون منطق قبلی + mutation یکدست) -----------------
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

    # -------- mutation helpers --------
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

    # -------- GA loop --------
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
            

            if n1 >= 2 and n2 >= 2:
                c1 = random.randint(2, n1)
                c2 = random.randint(2, n2)
                t1, t2 = swap_subtrees(t1, t2, c1, c2)

            # ✅ مهم: mutation با همان نرخ‌ها برای همه‌ی بچه‌ها
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


# ----------------- RUN -----------------
# 1) دیتاست ثابت
random.seed(INPUT_SEED)
input_data = create_input()

# 2) تکامل (اگر seed ثابت باشد خروجی تکراری می‌شود)
if EVOLUTION_SEED is None:
    random.seed()
else:
    random.seed(EVOLUTION_SEED)

functions = create_trees()
_, best_tree, best_mse = make_generation(functions, input_data, THRESHOLD)

print_tree(best_tree)
print(f"Best MSE after {THRESHOLD} generations is {best_mse}")
print("Best expression found:", tree_to_expr(best_tree))
