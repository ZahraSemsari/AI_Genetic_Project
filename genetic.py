import random



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
        input_output[input] = output 
    print(input_output)

# print(create_input())






