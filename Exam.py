#Var 4
#Вариант 4: Дан код на языке Python, выравнивание в котором выполнено при помощи пробелов, все операторы записаны в одну
# строку, классы не используются. Представьте этот код в виде дерева по следующему алгоритму. Корнем дерева является
# фиктивная вершина. Все строки кода с одинаковым отступом являются вершинами одного уровня. Родителем строки является
# последняя перед ней строка с уровнем отступа на один меньше, при этом считается не число пробелов, а факт увеличения
# их количества. Потомки идут в том порядке, в котором они записаны в файле.
#По заданному имени функции проверьте, является ли данная функция рекурсивной. В общем случае, условные конструкции, циклы и проч. не могут препятствовать вызову функции.

import re


def read_file(filename):
    with open(filename, encoding='utf-8') as f:
        script = f.read()
    script = re.sub('\n\s*\n', '\n', script)
    if script[-1] == '\n':
        script = script[:-1]
    return script.split('\n')


def hierarchy_script(script, tree, cur_lev, step=1):
    cur_d = 0
    for i in range(len(script)):
        line = script[i]
        if line[0] == ' ' and step == 1:
            ind = 1
            while line[ind] == ' ':
                step += 1
                ind += 1
        cur_lev, cur_d = add_line_to_tree(line, tree, cur_lev, cur_d, step)


def add_line_to_tree(line, tree, cur_lev, cur_d, step):
    depth = 0
    while line[step * depth] == ' ':
        depth += 1
    if depth == cur_d:
        cur_lev.append(line)
        return cur_lev, cur_d
    if depth > cur_d:
        cur_lev.append([line])
        return  cur_lev[-1], depth
    cur_lev = tree
    for i in range(depth):
        cur_lev = cur_lev[-1]
    cur_lev.append(line)
    return cur_lev, depth


def find_recursion(cur_lev, function, isfunc=False, isrec=False):
    for i in range(len(cur_lev)):
        if type(cur_lev[i]) == str:
            if re.search(rf'def {function}\(', cur_lev[i]):
                isfunc = True
                isrec = IsRecursion(cur_lev[i+1], function)
        else:
            isfunc, isrec = find_recursion(cur_lev[i], function, isfunc, isrec)
    return isfunc, isrec


def IsRecursion(cur_lev, function, isrec=False):
    for i in range(len(cur_lev)):
        if type(cur_lev[i]) == str:
            if re.search(rf'{function}\(', cur_lev[i]):
                return True
        else:
            isrec = IsRecursion(cur_lev[i], function, isrec)
    return isrec


def answer(data):
    isfunc, isrec = data[0], data[1]
    if not isfunc:
        return 'There is no such a function in the script'
    if isrec:
        return 'This function is recursive'
    return 'This function is not recursive'


def main():
    filename = input('Input filename: ')
    script = read_file(filename)
    tree = ['', []]
    hierarchy_script(script, tree[-1], tree[-1])
    function = input('Input function name: ')
    print(answer(find_recursion(tree, function)))


if __name__ == '__main__':
    main()