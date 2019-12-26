import random, copy
import numpy as np
import matplotlib.pyplot as plt


class MyProcess:
    # order = 0
    time_wait = 0
    # time_brust = 0
    def __init__(self, i, t):
        self.order = i
        self.time_brust = t


hypo_01_p_60_time = {
    'num': 60,
    'step':[[2,8],[20,30],[35,40]],
    'percentage':[0.7, 0.2, 0.1]
}
hypo_02_p_40_time = {
    'num': 40,
    'step':[[2,8],[20,30],[35,40]],
    'percentage':[0.5, 0.3, 0.2]
}
hypo_02_p_20_time = {
    'num': 20,
    'step':[[2,8],[20,30],[35,40]],
    'percentage':[0.4, 0.4, 0.2]
}

hypo_02_p_5_time = {
    'num': 5,
    'step':[[2,8],[20,30],[35,40]],
    'percentage':[0.4, 0.4, 0.2]
}

nervegear = {
    'num': 50,
    'step':[[2,8],[20,30],[35,40]],
    'percentage':[0.4, 0.4, 0.2]
}

process_test = [MyProcess(0,24), MyProcess(1,3), MyProcess(2,3)]

process_test_2 = [MyProcess(0,8), MyProcess(1,4), MyProcess(2,9),MyProcess(3,5)]


def random_process_time(time_and_percentage):
    """ สุ่มค่าให้กับ process """
    print("_________ Generate Brusttime in process _________")
    temp_process = []
    temp_print_brust = []
    for i in range(0, time_and_percentage['num']):
        rand_choice = __rand_choice(time_and_percentage)
        brust_time = __get_rand_time(rand_choice, time_and_percentage)
        temp_process.append(MyProcess(i, brust_time))
        temp_print_brust.append(brust_time)
    print(temp_print_brust)
    return temp_process


def __rand_choice(time_and_percentage):
    """ random choice to choose brut time probability """
    size_of_time_list = len(time_and_percentage['step'])
    percentage_prop_list = time_and_percentage['percentage']
    # random with probability by numpy function
    return np.random.choice(np.arange(0, size_of_time_list), p=percentage_prop_list)


def __get_rand_time(i, time_and_percentage):
    a = time_and_percentage['num']
    t  = time_and_percentage['step'][i]
    return np.random.randint(low=t[0], high=t[1])


def print_process(list_p):
    print("_________ Print Process _________")
    process_num = len(list_p)
    for i in range(0, process_num):
        #print("i= {:2d} bt= {:3d} wt= {:3d}".format(list_p[i].order,list_p[i].time_brust, list_p[i].time_wait))
        print("{}\t{}\t{}".format(list_p[i].order,list_p[i].time_brust, list_p[i].time_wait))
    print(">>Wait time: ",get_process_average(list_p)[0],"\n>>Average: ", get_process_average(list_p)[1])

def get_process_average(list_p):
    process_num = len(list_p)
    sum = __sum_process_wait_time(list_p)
    return [sum, sum/process_num]


def __sum_process_wait_time(list_p):
    sum = 0
    for p in list_p:
        sum += p.time_wait
    return sum



def first_come_first_served(list_p):
    temp_list_p = copy.deepcopy(list_p)
    print("_________ FCFS _________")
    process_num = len(temp_list_p)
    sum = 0
    for i in range(0, process_num):
        temp_list_p[i].time_wait += sum
        bt = temp_list_p[i].time_brust
        sum += bt
    return temp_list_p


def shortest_job_first(list_p):
    print("_________ SJF _________")
    # sorting
    dict_p = __extend_class_to_dict(list_p)
    sort_dict_p = __sorted_dict(dict_p)
    sort_list_p = __convert_dict_to_class(sort_dict_p)
    return first_come_first_served(sort_list_p)


def __extend_class_to_dict(list_p):
    temp_p = {}
    for p in list_p:
        temp_p[p.order] = p.time_brust
    return temp_p


def __sorted_dict(dict_p):
    from collections import OrderedDict
    sort_dicted = dict(OrderedDict(sorted(dict_p.items(), key=lambda t: t[1])))
    return sort_dicted


def __convert_dict_to_class(dict_p):
    temp_p = []
    for d in dict_p:
        temp_p.append(MyProcess(d, dict_p[d]))
    return temp_p


def round_robin(q, list_p):
    #print("_________ Round robin _________")
    from collections import deque
    new_p = deque(copy.deepcopy(list_p))
    que = []
    timeline = 0
    prev_timeline = 0
    while True:
        p = new_p.popleft()
        diff = p.time_brust - q
        if diff > 0:
            prev_timeline = timeline
            timeline += q
            p.time_brust = diff
            new_p.append(p)
        else:
            prev_timeline = timeline
            timeline += p.time_brust

        tmp = [p.order, [prev_timeline, timeline]]
        que.append(tmp)
        if len(new_p) <= 0:
            break

    rr_timeline = __rr_wait_time_comvert_timeline(q, que)
    rr_process_wait = __rr_wait_time(rr_timeline)
    #print(">> RR_ timeline\n", que)
    #print(">> RR Process Wait time\n", rr_process_wait)

    clone_list_p = copy.deepcopy(list_p)
    __rr_insert_wait_to_class(clone_list_p, rr_process_wait)

    return clone_list_p


def __rr_insert_wait_to_class(list_p ,rr_process_wait):
    for k in list_p:
        i = k.order
        k.time_wait = rr_process_wait[i]


def __rr_wait_time(rr_timeline):
    temp_dict_p = {}
    for rr_list in rr_timeline:
        time = 0
        is_see_first = False
        for i, tt in enumerate(rr_timeline[rr_list]):
            if tt[0] == 0:
                is_see_first = True
                time += tt[1]
            else:
                if is_see_first:
                    cal = (tt[0]- rr_timeline[rr_list][i-1][1])
                    time += cal
                    # print(rr_timeline[rr_list][i-1][1], tt[0],  '=', cal)
                else:
                    time += tt[0]
            # print(time)
        temp_dict_p[rr_list] = time
    return temp_dict_p



def __rr_wait_time_comvert_timeline(q, rr_que):
    data = {}
    for i,d in enumerate(rr_que):
        if d[0] not in data:
            data[d[0]] = [d[1]]
        else:
            data[d[0]].append(d[1])
    #print(data)
    return data

def find_best_quantum_time(stop, list_p):
    min_value = 9999999
    min_q = -1

    for i in range(1, stop):
        __list_p = round_robin(i, list_p)
        avr = get_process_average(__list_p)[1]
        if avr < min_value:
            min_value = avr
            min_q = i
    return min_q


def graph_plot_more(more_list_p, graph_name_list):
    __graph_list = []
    ppx_list = []

    for i, mp in enumerate(more_list_p):
        __process_wait_time = []
        for p in mp:
            __process_wait_time.append(p.time_wait)

        __graph_list.append(__process_wait_time)
        ppx = plt.plot(__process_wait_time, linestyle='--', label=graph_name_list[i])
        ppx_list.append(ppx)
    plt.legend(loc=2, borderaxespad=0.)
    print(__graph_list)




    plt.ylabel('Number of process and Wait time realation')
    plt.show()

def graph_plot(name, list_p):
    __process_wait_time = []
    for p in list_p:
        __process_wait_time.append(p.time_wait)

    plt.plot(__process_wait_time, linestyle='--', label=name)
    plt.ylabel(name)






if __name__ == '__main__':
    #process generate
    process = random_process_time(nervegear)

    avr = []

    pp = process
    print_process(pp)


    fcs = first_come_first_served(pp)
    sjf = shortest_job_first(pp)
    # find best quantum number
    rr_quantum = find_best_quantum_time(100,pp)
    rr_quantum = 30
    rrq = round_robin(rr_quantum, pp)
    rrq_10 = round_robin(10, pp)


    print("\n\n########## RESUALT ##########")
    print("\n--------- first_come_first_served -----------")
    print_process(fcs)
    avr.append(get_process_average(fcs))
    #graph_plot('first_come_first_served', fcs)

    print("\n--------- shortest_job_first -----------")
    print_process(sjf)
    avr.append(get_process_average(sjf))
    #graph_plot('shortest_job_first', sjf)

    print("\n--------- round_robin -----------")
    print_process(rrq)
    avr.append(get_process_average(rrq))
    #graph_plot('round_robin', rrq)


    graph_name = ['first_come_first_served', 'shortest_job_first', 'round_robin_with_q='+str(rr_quantum), 'round_robin_with_q=10']
    graph_name = ['first_come_first_served', 'shortest_job_first', '(best Q)round_robin_with_q='+str(rr_quantum)]
    graphs= [fcs, sjf, rrq, rrq_10]
    graphs= [fcs, sjf, rrq]
    graph_plot_more(graphs, graph_name)
    print(avr, "In quantum number=", rr_quantum)


