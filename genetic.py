import random
import math
random.seed(42)

class TreeNode():
    def __init__(self):
        self.child = []
        self.parent = None
        self.value = None



def create_input() :
    input_output = dict()
    input = 0
    for _ in range(0,45) :
        i = random.randint(0, 10)
        for k in input_output :
            if k == i :
                i = random.randint(0, 10)
            else :
                input = i

        output = input * input + 2 * input + 1
        input_output[input] = float(output) 
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
                if root.value[1] != 'sin' and root.value[0] != 'cos':
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
    for _ in range(1):
        rand = random.randint(0,6) 
        root = TreeNode()
        root.value = ['operator',OPERATOR_COEFFICIENT['operator'][rand]]
        root = create_tree(root , depth , max_depth)
        functions.append(root)
    
    print_tree(root)
    return functions


# create_trees()            


def compute_fitness() :
    def compute_MSE(ouput , input) :
        for index,i in enumerate(input) :
            MSE = (output[index] - input[i]) ** 2
        MSE = MSE / len(input)
        return MSE 
        

    def compute_fitnes(func , input) : 
        if len(func.child) == 0 :
            if func.value[1] == 'x' :
                return float(input)
            else :
                return func.value[1] 
        
        child_num = len(func.child)

        if child_num == 2 :
            first_opernad = float(compute_fitnes(func.child[0] , input))
            second_operand = float(compute_fitnes(func.child[1] , input))
            if func.value[1] == '*' :
                return first_opernad * second_operand
            elif func.value[1] == '+' :
                return first_opernad + second_operand            
            elif func.value[1] == '-' :
                return first_opernad - second_operand            
            elif func.value[1] == '/' :
                return first_opernad / second_operand            
            elif func.value[1] == 'pow' :
                return first_opernad ** second_operand   
        else :
            first_opernad = float(compute_fitnes(func.child[0] , input))
            if func.value[1] == 'sin' :
                return math.sin(first_opernad)
            elif func.value[1] == 'cos' :
                return math.cos(first_opernad)




    functions = create_trees()
    input = create_input()
    output = []
    mse_arr = []

    for f in functions :
        for i in input:
            output.append(compute_fitnes(f , i))
        print(output)
        mse = compute_MSE(output , input)
        mse_arr.append(mse)
    print(mse_arr)

compute_fitness()
