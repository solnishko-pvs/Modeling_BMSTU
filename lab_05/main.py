from random import random
from time import time
import tkinter as tk
from tkinter import ttk
from numpy.random import gamma
import random

MINVALUE_GEN = 1
MAXVALUE_GEN = 10000
MAXVALUE_LESS = MAXVALUE_GEN  # // 10
unit_of_time = 0.01
COLOR = '#dddddd'
MAX_SIZE = 10
WIDGET_WIDTH_1 = 30
WIDGET_WIDTH = 25

class EvenDistribution:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def generate(self):
        return self.a + (self.b - self.a) * random.random()


class Generator:
    def __init__(self, distribution):
        self.work_time_distribution = distribution
        self.time_to_finish = 0

    def upd_time(self, dt):
        self.time_to_finish -= dt

        if self.time_to_finish <= 1e-5:
            self.time_to_finish = self.work_time_distribution.generate()
            return Request()

        return None


class Operator:
    def __init__(self, send_to, distribution):
        self.work_time_distribution = distribution
        self.busy = False
        self.send_to = send_to
        self.current_req = None
        self.time_to_finish = 0

    def accept_request(self, request):
        self.busy = True
        self.current_req = request
        self.time_to_finish = self.work_time_distribution.generate()

    def finish_cur_request(self):
        self.send_to.append(self.current_req)
        self.busy = False
        self.current_req = None

    def upd_time(self, dt):
        self.time_to_finish -= dt
        if self.busy and self.time_to_finish <= 1e-5:
            self.finish_cur_request()
            return 'req fin'
        return 'pass'


class Processor:
    def __init__(self, requests_queue, distribution):
        self.work_time_distribution = distribution
        self.busy = False
        self.requests_queue = requests_queue
        self.current_req = None
        self.time_to_finish = 0

    def upd_time(self, dt):
        self.time_to_finish -= dt

        if self.busy and self.time_to_finish <= 1e-5:
            self.busy = False
            #print(self.current_req.id, 'proc')
            self.current_req = None
            return 'req fin'

        if not self.busy and len(self.requests_queue) != 0:
            self.current_req = self.requests_queue.pop(0)
            self.time_to_finish = self.work_time_distribution.generate()
            self.busy = True
            return 'req acc'

        return 'pass'


class Request:
    cur_id = 0

    def __init__(self):
        self.id = Request.cur_id
        Request.cur_id += 1


def pick_operator(operators):
    for i in range(len(operators)):
        if not operators[i].busy:
            return i
    return -1


def one_step(generator, operators, processors, request_info, generate_new=True):
    if generate_new:
        request = generator.upd_time(unit_of_time)
        if request:
            request_info['generated'] += 1
            i_operator = pick_operator(operators)
            if i_operator == -1:
                request_info['lost'] += 1
            else:
                operators[i_operator].accept_request(request)

    for cur_operator in operators:
        cur_operator.upd_time(unit_of_time)

    for cur_processor in processors:
        res = cur_processor.upd_time(unit_of_time)
        if res == 'req fin':
            request_info['processed'] += 1


def modeling(generator, operators, processors, total_incoming_requests):
    request_info = {'generated': 0, 'lost': 0, 'processed': 0}
    time = 0
    while request_info['generated'] < total_incoming_requests:
        one_step(generator, operators, processors, request_info)
        time += unit_of_time

    while request_info['lost'] + request_info['processed'] < total_incoming_requests:
        one_step(generator, operators, processors, request_info, False)
        time += unit_of_time

    return request_info, time


class FrameBlock:
    def __init__(self, master, text, row, column, rowspan=1, columnspan=1, def_from=1, def_to=1):
        self.frame_1 = tk.LabelFrame(master, bg=COLOR, text=text, width=90, height=100)
        self.lab2 = tk.Label(self.frame_1, bg=COLOR, width=WIDGET_WIDTH_1//2, text='от:')
        self.lab3 = tk.Label(self.frame_1, bg=COLOR, width=WIDGET_WIDTH_1//2, text='до:')
        self.from_ = ttk.Combobox(self.frame_1, width=WIDGET_WIDTH_1 // 2,
                                         values=[i for i in range(1, MAX_SIZE*10 + 1)],
                                         state='readonly')
        self.to_ = ttk.Combobox(self.frame_1, width=WIDGET_WIDTH_1 // 2,
                                         values=[i for i in range(1, MAX_SIZE*10 + 1)],
                                         state='readonly')

        self.from_.bind("<FocusIn>", self.defocus)
        self.from_.set(def_from)
        self.to_.bind("<FocusIn>", self.defocus)
        self.to_.set(def_to)

        self.frame_1.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, padx=5, pady=5)

        self.lab2.grid(row=0, column=0, padx=5, pady=5)
        self.lab3.grid(row=1, column=0, padx=5, pady=5)
        self.from_.grid(row=0, column=1, padx=5, pady=5)
        self.to_.grid(row=1, column=1, padx=5, pady=5)

    def get_info(self):
        return int(self.from_.get()), int(self.to_.get())

    @staticmethod
    def defocus(event):
        event.widget.master.focus_set()

class Block:
    def __init__(self, master):

        self.frame = tk.LabelFrame(master, bg=COLOR, text='Ввод данных', width=800, height=450)
        #self.frame.columnconfigure(0, weight=1)
        #self.frame.rowconfigure(0, weight=1)
        #self.frame.grid_propagate(False)

        self.calculate_result_btn = tk.Button(self.frame, text="Вычислить", width=WIDGET_WIDTH,
                                              bg=COLOR, command=self.solve)

        self.generator_info = FrameBlock(self.frame, 'Время поступления клиентов', 0, 2, 1, 2, 8, 12)
        self.operator_1 = FrameBlock(self.frame, '1-ый оператор обрабатывает клиента', 1, 0, 1, 2, 15, 25)
        self.operator_2 = FrameBlock(self.frame, '2-ой оператор обрабатывает клиента', 1, 2, 1, 2, 30, 50)
        self.operator_3 = FrameBlock(self.frame, '3-ий оператор обрабатывает клиента', 1, 4, 1, 2, 20, 60)

        self.processor_1 = FrameBlock(self.frame, '1-ый компьютер обрабатывает заявку', 2, 1, 1, 2, 15, 15)
        self.processor_2 = FrameBlock(self.frame, '2-ой компьютер обрабатывает заявку', 2, 3, 1, 2, 30, 30)

        self.count_req_lab = tk.Label(self.frame, bg=COLOR, width=WIDGET_WIDTH_1//2, text='Количество заявок:')
        self.count_req = ttk.Combobox(self.frame, width=WIDGET_WIDTH_1//2,
                                  values=[i for i in range(100, 10001, 100)],
                                  state='readonly')
        self.count_req.bind("<FocusIn>", self.defocus)
        self.count_req.set(300)
        self.count_req_lab.grid(row=6, column=2, columnspan=1)
        self.count_req.grid(row=6, column=3)

        self.result_frame = tk.LabelFrame(master, bg=COLOR, text='Результат', width=350, height=500)
        self.result_frame.grid_propagate(False)

        self.res_label = tk.Label(self.result_frame, bg=COLOR, width=WIDGET_WIDTH-4,
                                  text='Всего клиентов')
        self.res_label.grid(row=0, column=0,)
        self.res_label1 = tk.Label(self.result_frame, bg=COLOR, width=WIDGET_WIDTH-4,
                                  text='Обработано клиентов')
        self.res_label1.grid(row=1, column=0, )
        self.res_label2 = tk.Label(self.result_frame, bg=COLOR, width=WIDGET_WIDTH-4,
                                  text='Потеряно клиентов')
        self.res_label2.grid(row=2, column=0, )
        self.res_label3 = tk.Label(self.result_frame, bg=COLOR, width=WIDGET_WIDTH - 4,
                                   text='Процент потерь')
        self.res_label3.grid(row=3, column=0, )
        self.res_label5 = tk.Label(self.result_frame, bg=COLOR, width=WIDGET_WIDTH - 4,
                                   text='Протянутое время, мин')
        self.res_label5.grid(row=4, column=0, )
        self.res_label4 = tk.Label(self.result_frame, bg=COLOR, width=WIDGET_WIDTH +5,
                                   text='Время работы программы, с')
        self.res_label4.grid(row=5, column=0, )


        self.step_label_res = tk.Label(self.result_frame, bg=COLOR, width=WIDGET_WIDTH-15,
                                       text='')
        self.step_label_res.grid(row=0, column=1)
        self.step_label_res1 = tk.Label(self.result_frame, bg=COLOR, width=WIDGET_WIDTH - 15,
                                       text='')
        self.step_label_res1.grid(row=1, column=1)
        self.step_label_res2 = tk.Label(self.result_frame, bg=COLOR, width=WIDGET_WIDTH - 15,
                                       text='')
        self.step_label_res2.grid(row=2, column=1)

        self.step_label_res3 = tk.Label(self.result_frame, bg=COLOR, width=WIDGET_WIDTH - 15,
                                        text='')
        self.step_label_res3.grid(row=3, column=1)
        self.step_label_res4 = tk.Label(self.result_frame, bg=COLOR, width=WIDGET_WIDTH - 15,
                                        text='')
        self.step_label_res4.grid(row=4, column=1)
        self.step_label_res5 = tk.Label(self.result_frame, bg=COLOR, width=WIDGET_WIDTH - 15,
                                        text='')
        self.step_label_res5.grid(row=5, column=1)

        # self.lab.grid(row=0, column=0)
        # self.matrix_size.grid(row=0, column=1)

        self.calculate_result_btn.grid(row=8, column=2, columnspan=2,  pady=5)
        # self.listbox.grid(row=4, column=0, columnspan=10)

    @staticmethod
    def defocus(event):
        event.widget.master.focus_set()

    def make_view(self):
        # self.frame.grid(row=row, column=column)
        self.frame.pack()
        # self.listbox_frame.grid(row=3, column=0, columnspan=10)
        self.result_frame.pack(pady=5)

    def solve(self):
        gen = self.generator_info.get_info()
        client_generator = Generator(EvenDistribution(gen[0], gen[1]))

        first_queue = []
        second_queue = []

        operators = [
            Operator(first_queue, EvenDistribution(*self.operator_1.get_info())),  # самый производительный
            Operator(first_queue, EvenDistribution(*self.operator_2.get_info())),
            Operator(second_queue, EvenDistribution(*self.operator_3.get_info()))  # наименее производительный
        ]

        processors = [
            Processor(first_queue, EvenDistribution(*self.processor_1.get_info())),  # ровно 15 минут
            Processor(second_queue, EvenDistribution(*self.processor_2.get_info()))  # ровно 30 минут
        ]

        total_requests = int(self.count_req.get())

        t_start = time()
        res, t = modeling(client_generator, operators, processors, total_requests)

        self.step_label_res['text'] = str(res['generated'])
        self.step_label_res1['text'] = str(res['processed'])
        self.step_label_res2['text'] = str(res['lost'])
        self.step_label_res3['text'] = str(round(res['lost'] / total_requests * 100, 3)) + ' %'
        self.step_label_res4['text'] = str(round(t, 2))
        self.step_label_res5['text'] = str(round(time() - t_start, 2))

        #
        # print('time seconds', time() - t_start)
        # for key in res.keys():
        #     print(key, res[key])
        #
        # print('lost', res['lost'] / total_requests)
        # print(t)


# print(calculate(np.matrix([[0.0, 0.559, 0.2709],[0.5025, 0.0, 0.0507],[0.7526, 0.2594, 0.0]])))

root = tk.Tk()
root['bg'] = COLOR
root.geometry('800x510')
# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)

first_block = Block(root)
first_block.make_view()
# second_block = Block(root, 'str_reverse')
root.mainloop()