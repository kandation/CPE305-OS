import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Frame:
    frame = []
    def __init__(self, max_frame):
        self.max_frame = max_frame

    def insert(self,v):
        if len(self.frame) < self.max_frame:
            self.frame.append(v)
            return 1

def ref_string_test(L, f):
    return [7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1]


def ref_string_random(L, k):
    return np.random.randint(k,size=L).tolist()

def ref_string_sorted(L ,k):
    n = L//k
    list_num = []
    if L > k:
        # loop post number
        for i in range(0, k-1):
            for j in range(0, n):
                list_num.append(i)

        #loop last number overwise
        last_other = L - len(list_num)
        for a in range(0, last_other):
            list_num.append(k-1)
    else:
        for i in range(0, L):
            list_num.append(i)

    return list_num

def ref_string_frammed(L, f):
    num = []
    for i in range(0, L):
        for j in range(0, f):
            num.append(j)
    num = num[0:L]
    return num




def fifo(list_ref, frame_size):
    frame = []
    history_page_fault = []

    stat_page_fault = 0
    stat_graph = {'x':[], 'y':[]}

    # loop all reference string
    for i,v in enumerate(list_ref):

        # if frame not full u can insert any and give 1 pages fault
        if len(frame) < frame_size:
            frame.append(v)
            stat_page_fault += 1
            history_page_fault.append(frame.copy())

        else:
            # when frame is full look some page and replace
            if v not in frame:
                stat_page_fault += 1
                frame.pop(0)
                frame.append(v)
                history_page_fault.append(frame.copy())

        # get stat for grap
        stat_graph['x'].append(i)
        stat_graph['y'].append(stat_page_fault)

    return [stat_page_fault, stat_graph, history_page_fault]


def optimal(list_ref, frame_size):
    frame = []
    history_page_fault = []

    stat_page_fault = 0
    stat_graph = {'x': [], 'y': []}

    # loop all reference string
    for i, v in enumerate(list_ref):

        # if frame not full u can insert any and give 1 pages fault
        if len(frame) < frame_size:
            frame.append(v)
            stat_page_fault += 1
            history_page_fault.append(frame.copy())

        else:
            # when frame is full look some page and replace
            if v not in frame:
                tmp_stat_page_found = []

                # loop pages in frame
                for p in frame:
                    next_found = __optimal_searcher(list_ref[i+1:len(list_ref)], p)
                    tmp_stat_page_found.append(next_found)

                #find longest number
                (value_max,index_max) = max((vv,ii) for ii,vv in enumerate(tmp_stat_page_found))

                # replace value in frame list
                frame[index_max] = v
                stat_page_fault += 1
                history_page_fault.append(frame.copy())
        stat_graph['x'].append(i)
        stat_graph['y'].append(stat_page_fault)
    return [stat_page_fault, stat_graph, history_page_fault]


def __optimal_searcher(list_ref_section, v):
    for i in range(0, len(list_ref_section)):
        if list_ref_section[i] == v:
            return i
    return 99999999



def lru(list_ref, frame_size):
    frame = []
    history_page_fault = []

    stat_page_fault = 0
    stat_graph = {'x': [], 'y': []}

    # loop all reference string
    for i, v in enumerate(list_ref):

        # if frame not full u can insert any and give 1 pages fault
        if len(frame) < frame_size:
            frame.append(v)
            stat_page_fault += 1
            history_page_fault.append(frame.copy())


        else:
            # when a frame is full look some page for replace
            if v not in frame:
                tmp_stat_page_found = []

                # loop data in frame and find longest distanct in pass for nex replace
                for p in frame:
                    prev_list = list_ref[0:i]
                    prev_page_found = __lru_couter(prev_list, p)
                    tmp_stat_page_found.append(prev_page_found)


                # find longest number
                (value_max, index_max) = max((vv, ii) for ii, vv in enumerate(tmp_stat_page_found))

                # replace value in frame list
                frame[index_max] = v
                stat_page_fault += 1
                history_page_fault.append(frame.copy())

        stat_graph['x'].append(i)
        stat_graph['y'].append(stat_page_fault)
    return [stat_page_fault, stat_graph, history_page_fault]


def __lru_couter(prev_list, key):
    # lru counter
    couter = 0
    for i, e in reversed(list(enumerate(prev_list))):
        if prev_list[i] == key:
            return couter
        couter += 1
    return 99999999

def print_data_raw(data_ref_string_list):
    for i,v in enumerate(data_ref_string_list):
        print(i+1,'\t', v)
    print("________________________________________________")

def print_graph_2d(graph_list, title):
    for g in graph_list:
        #print(g)
        plt.plot(g['x'],g['y'], label=g['name'],linestyle='dotted')
        plt.title(title['name'])
        plt.xlabel(title['x'])
        plt.ylabel(title['y'])
        plt.legend()
        if title['s']:
            plt.show()
    if not title['s']:
        plt.show()



def experiment_01_1(n, page_charecter_num , spl=False):
    # ss.01 graph show relative size_of(ref_string) and num_page_fault
    data_ref_string_list = []
    algor_graph_save = []

    # number of frame
    f = 3

    #generate Refernce String data Set
    for i in range(1, n+1):
        referance_string = ref_string_sorted(i, page_charecter_num)
        data_ref_string_list.append(referance_string.copy())

    #run fifo
    graph_ss_01 = {'name':"FIFO",'x': [], 'y': []}
    for i in range(1, n+1):
        r = fifo(data_ref_string_list[i-1], f)
        graph_ss_01['x'].append(i)
        graph_ss_01['y'].append(r[0])
    algor_graph_save.append(graph_ss_01.copy())

    #run optimal
    graph_ss_01 = {'name': "Optimal", 'x': [], 'y': []}
    for i in range(1, n + 1):
        j = optimal(data_ref_string_list[i-1], f)
        graph_ss_01['x'].append(i)
        graph_ss_01['y'].append(j[0])
    algor_graph_save.append(graph_ss_01.copy())

    #run LRU
    graph_ss_01 = {'name': "LRU", 'x': [], 'y': []}
    for i in range(1, n + 1):
        q = lru(data_ref_string_list[i-1], f)
        graph_ss_01['x'].append(i)
        graph_ss_01['y'].append(q[0])
    algor_graph_save.append(graph_ss_01.copy())


    # show result
    print_data_raw(data_ref_string_list)
    title = {
        'name': "Relative between len(ref String) and num(pageFault) with c="+str(page_charecter_num)+" f="+str(f),
        'x': 'length refernce string',
        'y': 'Number of page fault',
        's': spl
    }
    print_graph_2d(algor_graph_save, title)


def experiment_01_2(n ,c, spl=False):
    data_ref_string_list = []
    algor_graph_save = []

    # number of frame
    f = c

    #generate Refernce String data Set
    for i in range(1, n+1):
        referance_string = ref_string_frammed(i, c)
        data_ref_string_list.append(referance_string.copy())

    #run fifo
    graph_ss_01 = {'name':"FIFO",'x': [], 'y': []}
    for i in range(1, n+1):
        r = fifo(data_ref_string_list[i-1], f)
        graph_ss_01['x'].append(i)
        graph_ss_01['y'].append(r[0])
    algor_graph_save.append(graph_ss_01.copy())

    #run optimal
    graph_ss_01 = {'name': "Optimal", 'x': [], 'y': []}
    for i in range(1, n + 1):
        j = optimal(data_ref_string_list[i-1], f)
        graph_ss_01['x'].append(i)
        graph_ss_01['y'].append(j[0])
    algor_graph_save.append(graph_ss_01.copy())

    #run LRU
    graph_ss_01 = {'name': "LRU", 'x': [], 'y': []}
    for i in range(1, n + 1):
        q = lru(data_ref_string_list[i-1], f)
        graph_ss_01['x'].append(i)
        graph_ss_01['y'].append(q[0])
    algor_graph_save.append(graph_ss_01.copy())


    # show result
    title = {
        'name':"Relative between len(Ref String) and num(PageFault) with c="+str(c)+" f="+str(f),
        'x':'Length of refernce string',
        'y':'Number of page fault',
        's': spl
    }
    print_data_raw(data_ref_string_list)
    print_graph_2d(algor_graph_save, title)


def experiment_01_3(ref_list,n, page_charecter_num , spl=False):
    # ss.01 graph show relative size_of(ref_string) and num_page_fault
    data_ref_string_list = []
    algor_graph_save = []

    # number of frame
    f = 3

    #generate Refernce String data Set
    for i in range(1, n+1):
        referance_string = ref_list[0:i]
        data_ref_string_list.append(referance_string.copy())

    #run fifo
    graph_ss_01 = {'name':"FIFO",'x': [], 'y': []}
    for i in range(1, n+1):
        r = fifo(data_ref_string_list[i-1], f)
        graph_ss_01['x'].append(i)
        graph_ss_01['y'].append(r[0])
    algor_graph_save.append(graph_ss_01.copy())

    #run optimal
    graph_ss_01 = {'name': "Optimal", 'x': [], 'y': []}
    for i in range(1, n + 1):
        j = optimal(data_ref_string_list[i-1], f)
        graph_ss_01['x'].append(i)
        graph_ss_01['y'].append(j[0])
    algor_graph_save.append(graph_ss_01.copy())

    #run LRU
    graph_ss_01 = {'name': "LRU", 'x': [], 'y': []}
    for i in range(1, n + 1):
        q = lru(data_ref_string_list[i-1], f)
        graph_ss_01['x'].append(i)
        graph_ss_01['y'].append(q[0])
    algor_graph_save.append(graph_ss_01.copy())


    # show result

    title = {
        'name':"Relative between len(ref) and num(PageFault) with c="+str(page_charecter_num)+" f="+str(f),
        'x':'Length of refernce string',
        'y':'Number of page fault',
        's': spl
    }
    print_data_raw(data_ref_string_list)
    print_graph_2d(algor_graph_save, title)


def experiment_02_1(n, page_charecter_num , spl=False):
    # ss.01 graph show relative size_of(ref_string) and num_page_fault
    data_ref_string_list = []
    algor_graph_save = []


    #generate Refernce String data Set
    referance_string = ref_string_sorted(n, page_charecter_num)
    data_ref_string_list.append(referance_string.copy())

    #run fifo
    graph_ss_01 = {'name':"FIFO Graph",'x': [], 'y': []}
    for i in range(1, n+1):
        r = fifo(referance_string, i)
        graph_ss_01['x'].append(i)
        graph_ss_01['y'].append(r[0])
    algor_graph_save.append(graph_ss_01.copy())

    #run optimal
    graph_ss_01 = {'name': "Optimal Graph", 'x': [], 'y': []}
    for i in range(1, n + 1):
        j = optimal(referance_string, i)
        graph_ss_01['x'].append(i)
        graph_ss_01['y'].append(j[0])
    algor_graph_save.append(graph_ss_01.copy())

    #run LRU
    graph_ss_01 = {'name': "LRU Graph", 'x': [], 'y': []}
    for i in range(1, n + 1):
        q = lru(referance_string, i)
        graph_ss_01['x'].append(i)
        graph_ss_01['y'].append(q[0])
    algor_graph_save.append(graph_ss_01.copy())

    print(len(algor_graph_save))
    # show result
    print_data_raw(data_ref_string_list)
    title = {
        'name': "Relative between num(Frames) and num(PageFault) with c="+str(page_charecter_num)+" p=SORTED",
        'x': 'Number of Frames',
        'y': 'Number of page fault',
        's': spl
    }
    print_graph_2d(algor_graph_save, title)

def experiment_02_2(n, page_charecter_num , spl=False):
    # ss.01 graph show relative size_of(ref_string) and num_page_fault
    data_ref_string_list = []
    algor_graph_save = []


    #generate Refernce String data Set
    referance_string = ref_string_frammed(n, page_charecter_num)
    data_ref_string_list.append(referance_string.copy())

    #run fifo
    graph_ss_01 = {'name':"FIFO",'x': [], 'y': []}
    for i in range(1, n+1):
        r = fifo(referance_string, i)
        graph_ss_01['x'].append(i)
        graph_ss_01['y'].append(r[0])
    algor_graph_save.append(graph_ss_01.copy())

    #run optimal
    graph_ss_01 = {'name': "Optimal", 'x': [], 'y': []}
    for i in range(1, n + 1):
        j = optimal(referance_string, i)
        graph_ss_01['x'].append(i)
        graph_ss_01['y'].append(j[0])
    algor_graph_save.append(graph_ss_01.copy())

    #run LRU
    graph_ss_01 = {'name': "LRU", 'x': [], 'y': []}
    for i in range(1, n + 1):
        q = lru(referance_string, i)
        graph_ss_01['x'].append(i)
        graph_ss_01['y'].append(q[0])
    algor_graph_save.append(graph_ss_01.copy())

    print(len(algor_graph_save))
    # show result
    print_data_raw(data_ref_string_list)
    title = {
        'name': "Relative between num(Frames) and num(PageFault) with c="+str(page_charecter_num)+" p=FORMED",
        'x': 'Number of Frames',
        'y': 'Number of page fault',
        's': spl
    }
    print_graph_2d(algor_graph_save, title)


def experiment_02_3(n, page_charecter_num , spl=False):
    # ss.01 graph show relative size_of(ref_string) and num_page_fault
    data_ref_string_list = []
    algor_graph_save = []


    #generate Refernce String data Set
    referance_string = ref_string_random(n, page_charecter_num)
    data_ref_string_list.append(referance_string.copy())

    #run fifo
    graph_ss_01 = {'name':"FIFO",'x': [], 'y': []}
    for i in range(1, n+1):
        r = fifo(referance_string, i)
        graph_ss_01['x'].append(i)
        graph_ss_01['y'].append(r[0])
    algor_graph_save.append(graph_ss_01.copy())

    #run optimal
    graph_ss_01 = {'name': "Optimal", 'x': [], 'y': []}
    for i in range(1, n + 1):
        j = optimal(referance_string, i)
        graph_ss_01['x'].append(i)
        graph_ss_01['y'].append(j[0])
    algor_graph_save.append(graph_ss_01.copy())

    #run LRU
    graph_ss_01 = {'name': "LRU", 'x': [], 'y': []}
    for i in range(1, n + 1):
        q = lru(referance_string, i)
        graph_ss_01['x'].append(i)
        graph_ss_01['y'].append(q[0])
    algor_graph_save.append(graph_ss_01.copy())

    print(len(algor_graph_save))
    # show result
    print_data_raw(data_ref_string_list)
    title = {
        'name': "Relative between num(Frames) and num(PageFault) with c="+str(page_charecter_num)+" p=RANDOM",
        'x': 'Number of Frames',
        'y': 'Number of page fault',
        's': spl
    }
    print_graph_2d(algor_graph_save, title)



def experiment_03(n, num_frame, spl=False):
    # ss.01 graph show relative size_of(ref_string) and num_page_fault
    data_ref_string_list = []
    algor_graph_save = []



    #generate Refernce String data Set
    referance_string = ref_string_sorted(n, 19)
    data_ref_string_list.append(referance_string.copy())

    #run fifo
    graph_ss_01 = {'name':"FIFO Graph",'x': [], 'y': []}
    r = fifo(referance_string, num_frame)
    graph_ss_01['x'] = r[1]['x']
    graph_ss_01['y'] = r[1]['y']
    algor_graph_save.append(graph_ss_01.copy())

    # run optimal
    graph_ss_01 = {'name': "Optimal Graph", 'x': [], 'y': []}

    j = optimal(referance_string, num_frame)
    graph_ss_01['x'] = j[1]['x']
    graph_ss_01['y'] = j[1]['y']
    algor_graph_save.append(graph_ss_01.copy())

    # #run LRU
    graph_ss_01 = {'name': "LRU Graph", 'x': [], 'y': []}
    q = lru(referance_string, num_frame)
    graph_ss_01['x'] = q[1]['x']
    graph_ss_01['y'] = q[1]['y']
    algor_graph_save.append(graph_ss_01.copy())
    # show result

    title = {
        'name': "Relative between Frames and nPageFault with ratio L:f="+str(n)+":"+str(num_frame),
        'x': 'Lenght of Reference String',
        'y': 'Number of page fault',
        's': spl
    }
    print_data_raw(data_ref_string_list)
    print_graph_2d(algor_graph_save, title)


def experiment_04(max_ref_len, page_charecter_num , f, spl=False):
    # ss.01 graph show relative size_of(ref_string) and num_page_fault
    data_ref_string_list = []
    algor_graph_save = []

    # number of frame
    n = page_charecter_num

    #generate Refernce String data Set
    for i in range(1, n+1):
        referance_string = ref_string_random(max_ref_len, i)
        data_ref_string_list.append(referance_string.copy())

    #run fifo
    graph_ss_01 = {'name':"FIFO",'x': [], 'y': []}
    for i in range(1, n+1):
        r = fifo(data_ref_string_list[i-1], f)
        graph_ss_01['x'].append(i)
        graph_ss_01['y'].append(r[0])
    algor_graph_save.append(graph_ss_01.copy())

    #run optimal
    graph_ss_01 = {'name': "Optimal", 'x': [], 'y': []}
    for i in range(1, n + 1):
        j = optimal(data_ref_string_list[i-1], f)
        graph_ss_01['x'].append(i)
        graph_ss_01['y'].append(j[0])
    algor_graph_save.append(graph_ss_01.copy())

    #run LRU
    graph_ss_01 = {'name': "LRU", 'x': [], 'y': []}
    for i in range(1, n + 1):
        q = lru(data_ref_string_list[i-1], f)
        graph_ss_01['x'].append(i)
        graph_ss_01['y'].append(q[0])
    algor_graph_save.append(graph_ss_01.copy())


    # show result
    print_data_raw(data_ref_string_list)
    title = {
        'name': "max(c)="+str(page_charecter_num)+" f="+str(f)+" L="+str(max_ref_len),
        'x': 'various of(pageNum)',
        'y': 'Number of page fault',
        's': spl
    }
    print_graph_2d(algor_graph_save, title)


""" SS01 More Ref String """
# experiment_01_1(100 ,10)
# experiment_01_2(100, c=10)

# ex01_ref = ref_string_random(100, 10)
# experiment_01_3(ex01_ref, 100, 10)


""" SS02 More Frame """
# experiment_02_1(100, 10)
# experiment_02_2(100, 10)
# experiment_02_3(100, 10)

""" SS003 as randomly More various """
experiment_04(100, 10, f=3)
experiment_04(1000, 10, f=3)

experiment_04(100, 10, f=5)
experiment_04(1000, 10, f=5)

experiment_04(100, 10, f=8)
experiment_04(1000, 10, f=8)

experiment_04(100, 10, f=10)
experiment_04(1000, 10, f=10)

experiment_04(100, 100, f=10)
experiment_04(100, 500, f=10)
experiment_04(100, 1000, f=10)

experiment_04(1000, 100, f=10)


""" As random String L and f ratio (Not try)"""
# experiment_03(50, 3)
# experiment_03(50, 5)
# experiment_03(1000, 8)
#
#
# experiment_03(2, 1)
# experiment_03(20, 10)
# experiment_03(200, 100)
#
# experiment_03(10, 10)
# experiment_03(100, 100)
# experiment_03(200, 200)
#
# experiment_03(10, 20)
# experiment_03(200, 100)

# experiment_03(1, 10)
# experiment_03(10, 100)
# experiment_03(50, 500)


