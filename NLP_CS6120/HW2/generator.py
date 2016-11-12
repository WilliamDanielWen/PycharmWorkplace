import random

def read_grammar_file(grammar_file_name):
    f = open(grammar_file_name+".txt",'r')
    content = f.readlines()
    # Format : grammar[l_side]=(weight,r_side)
    #l_side is a non terminal
    #r_side is all the right hand side
    grammar = dict()
    for line in content:
        line = line.strip()
        if len(line)== 0: continue
        if line[0] == "#": continue
        rule = line.split()
        weigh = int(rule[0])
        l_side = rule[1]
        r_side = rule[2:]
        if l_side not in grammar: grammar[l_side] = []
        grammar[l_side].append((weigh,r_side))

    return grammar


def choose_Rside_withProb(grammar, l_side):
    weighted_choices = grammar[l_side]
    # creat a population according to the weight
    population =[]
    for weight, r_side in weighted_choices:
        if weight == 0: continue
        for i in range(weight):
            population.append(r_side)


    prob_r_side=random.choice(population)
    return prob_r_side


def generate_sentence(grammar):
    s_l_side = "START"
    output=""
    dfs_queue= []
    s_rside = choose_Rside_withProb(grammar, s_l_side)
    dfs_queue = s_rside+dfs_queue

    while len (dfs_queue) > 0:
        #symbol on the right hand side
        r_symbol = dfs_queue.pop(0)

        if not r_symbol in grammar:
            # symbol is a terminator
            output += r_symbol + " "
            continue

        #symbol is not a terminator
        new_symbols = choose_Rside_withProb(grammar, r_symbol)
        dfs_queue = new_symbols + dfs_queue

    return output

import sys
if __name__ == "__main__":
    #arg 0 is python script file name
    mode = "bash"
    mode = "python_script"

    if mode=="bash":
        if len(sys.argv) != 3:
            print("   wrong format of bash parameter!")
            print("   Usage:   ./generate [grammar file name] [number of sentences]" )
            exit(0)
        grammar_file_name=sys.argv[1]
        num_sentences=int(sys.argv[2])

        grammar=read_grammar_file(grammar_file_name)
        for i in range(num_sentences):
            print("No.",i+1,"sentence:")
            print(generate_sentence(grammar))
            print("")
    else:
        grammar_file_name = "grammar3"
        num_sentences = 100

        grammar = read_grammar_file(grammar_file_name)
        for i in range(num_sentences):
            #print("No.", i + 1, "sentence:")
            print(generate_sentence(grammar))
            print("")