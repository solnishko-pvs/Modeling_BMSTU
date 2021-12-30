import tkinter as tk
from tkinter import ttk
from numpy.random import normal
import random
from random import randint

MINVALUE_GEN = 1
MAXVALUE_GEN = 10000
MAXVALUE_LESS = MAXVALUE_GEN
COLOR = '#dddddd'
COLUMNS_COLOR = '#ffffff'
MAX_SIZE = 10
WIDGET_WIDTH = 25


class EvenDistribution:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def generate(self):
        return self.a + (self.b - self.a) * random.random()


class NormalDistribution:
    def __init__(self, lambda_):
        self.lambda_ = lambda_

    def generate(self):
        return normal(self.lambda_, self.lambda_**0.5)


def add_event(events, event):
    i = 0
    while i < len(events) and events[i][0] < event[0]:
        i += 1
    if 0 < i < len(events):
        events.insert(i - 1, event)
    else:
        events.insert(i, event)


def event_model(generator, processor, total_tasks=0, repeat=0):
    processed_tasks = 0
    cur_queue_len = max_queue_len = 0
    events = [[generator.generate(), 'g']]
    free, process_flag = True, False
    generated_tasks = 0
    repeated_tasks = 0

    while processed_tasks < total_tasks + repeated_tasks:
        event = events.pop(0)
        if event[1] == 'g' and generated_tasks <= total_tasks:
            cur_queue_len += 1
            generated_tasks += 1
            if cur_queue_len > max_queue_len:
                max_queue_len = cur_queue_len
            add_event(events, [event[0] + generator.generate(), 'g'])
            if free:
                process_flag = True
        elif event[1] == 'p':
            processed_tasks += 1
            if randint(1, 100) <= repeat:
                repeated_tasks += 1
                cur_queue_len += 1
            process_flag = True
        if process_flag:
            if cur_queue_len > 0:
                cur_queue_len -= 1
                t = processor.generate()
                # print(t)
                add_event(events, [event[0] + t, 'p'])
                free = False
            else:
                free = True
            process_flag = False

    return max_queue_len, processed_tasks, repeated_tasks


def step_model(generator, processor, total_tasks=0, repeat=0, step=0.001):
    processed_tasks = 0
    t_curr = step
    t_gen = generator.generate()
    t_proc = 0
    cur_queue_len = max_queue_len = 0
    generated_tasks = 0
    repeated_tasks = 0
    while processed_tasks < total_tasks + repeated_tasks:
        if t_curr > t_gen and generated_tasks <= total_tasks:
            cur_queue_len += 1
            generated_tasks += 1
            if cur_queue_len > max_queue_len:
                max_queue_len = cur_queue_len
            t_gen += generator.generate()
        if t_curr > t_proc:
            if cur_queue_len > 0:
                processed_tasks += 1
                if random.randint(1, 100) <= repeat:
                    repeated_tasks += 1
                    cur_queue_len += 1
                cur_queue_len -= 1
                t_proc += processor.generate()
        t_curr += step
    return max_queue_len, processed_tasks, repeated_tasks


class Block:
    def __init__(self, master):
        self.frame = tk.Frame(master, bg=COLOR, width=300, height=250)

        self.calculate_result_btn = tk.Button(self.frame, text="Вычислить", width=WIDGET_WIDTH, bg=COLOR, command=self.solve)
        self.lab = tk.Label(self.frame, bg=COLOR, width=WIDGET_WIDTH, text='Количество заявок:')
        self.lab1 = tk.Label(self.frame, bg=COLOR, width=WIDGET_WIDTH, text='Процент повторений:')
        self.frame_1 = tk.Frame(self.frame, bg=COLOR, width=300, height=100)
        self.titlepuss = tk.Label(self.frame_1, bg=COLOR, width=WIDGET_WIDTH, text = 'Распределение Пуассона')
        self.lab2 = tk.Label(self.frame_1, bg=COLOR, width=WIDGET_WIDTH, text='Лямбда:')
        self.frame_2 = tk.Frame(self.frame, bg=COLOR,  width=300, height=100)
        self.titleravn = tk.Label(self.frame_2, bg=COLOR, width=WIDGET_WIDTH, text='Равномерное распределение')
        self.lab4 = tk.Label(self.frame_2, bg=COLOR, width=WIDGET_WIDTH, text='a:')
        self.lab5 = tk.Label(self.frame_2, bg=COLOR, width=WIDGET_WIDTH, text='b:')
        self.lab.grid(row=0, column=0)
        self.lab1.grid(row=1, column=0)
        self.frame_1.grid(row=2, column=0, rowspan=3, columnspan=2, pady=5)
        self.lab2.grid(row=1, column=0)
        self.titlepuss.grid(row=0, column=0, columnspan=2, pady=5)
        self.frame_2.grid(row=5, column=0, rowspan=3, columnspan=2, pady=5)
        self.lab4.grid(row=1, column=0)
        self.titleravn.grid(row=0, column=0, columnspan=2, pady=5)
        self.lab5.grid(row=2, column=0)
        self.style = ttk.Style()
        self.style.configure('TCombobox', fieldbackground=COLOR)
        self.request_size = ttk.Combobox(self.frame, width=WIDGET_WIDTH//2,values=[i * 1000 for i in range(1, MAX_SIZE+1)], state='readonly')
        self.repeat_size = ttk.Combobox(self.frame, width=WIDGET_WIDTH//2, values=[i * 10 for i in range(0, MAX_SIZE + 1)], state='readonly')
        self.request_size.grid(row=0, column=1, padx=5)
        self.repeat_size.grid(row=1, column=1, padx=5)
        self.lambda_ = ttk.Combobox(self.frame_1, width=WIDGET_WIDTH//3, values=[1, 2, 3, 5, 7, 11], state='readonly')
        self.lambda_.grid(row=1, column=1, padx=5, sticky=tk.W)
        self.a_ = ttk.Combobox(self.frame_2, width=WIDGET_WIDTH//3, values=[i for i in range(1, MAX_SIZE + 1)], state='readonly')
        self.b_ = ttk.Combobox(self.frame_2, width=WIDGET_WIDTH//3, values=[i for i in range(1, MAX_SIZE + 1)],  state='readonly')
        self.a_.grid(row=1, column=1, padx=5, sticky=tk.W)
        self.b_.grid(row=2, column=1, padx=5, sticky=tk.W)
        self.request_size.bind("<FocusIn>", self.defocus)
        self.request_size.set(5000)
        self.repeat_size.bind("<FocusIn>", self.defocus)
        self.repeat_size.set(30)
        self.lambda_.bind("<FocusIn>", self.defocus)
        self.lambda_.set(3)
        self.a_.bind("<FocusIn>", self.defocus)
        self.a_.set(1)
        self.b_.bind("<FocusIn>", self.defocus)
        self.b_.set(5)
        self.result_frame = tk.Frame(master, bg=COLOR, width=600, height=100)
        self.result_frame.grid_propagate(False)
        self.res_label = tk.Label(self.result_frame, bg=COLOR, width=WIDGET_WIDTH-4, text='Максимальное количество\n заявок в очереди')
        self.res_label.grid(row=0, column=1,)
        self.res_label1 = tk.Label(self.result_frame, bg=COLOR, width=WIDGET_WIDTH-4, text='Всего обработано заявок')
        self.res_label1.grid(row=0, column=2, )
        self.res_label2 = tk.Label(self.result_frame, bg=COLOR, width=WIDGET_WIDTH-4, text='Количество отправленных\nназад в очередь заявок')
        self.res_label2.grid(row=0, column=3, )
        self.step_label = tk.Label(self.result_frame, bg=COLOR, width=WIDGET_WIDTH-9, text='Пошаговая модель:')
        self.step_label.grid(row=1, column=0)
        self.event_label = tk.Label(self.result_frame, bg=COLOR, width=WIDGET_WIDTH-9, text='Событийная модель:')
        self.event_label.grid(row=2, column=0)
        self.step_label_res = tk.Label(self.result_frame, bg=COLOR, width=WIDGET_WIDTH-15, text='', borderwidth=2, relief="groove")
        self.step_label_res.grid(row=1, column=1)
        self.step_label_res1 = tk.Label(self.result_frame, bg=COLOR, width=WIDGET_WIDTH - 15, text='', borderwidth=2, relief="groove")
        self.step_label_res1.grid(row=1, column=2)
        self.step_label_res2 = tk.Label(self.result_frame, bg=COLOR, width=WIDGET_WIDTH - 15, text='', borderwidth=2, relief="groove")
        self.step_label_res2.grid(row=1, column=3)
        self.event_label_res = tk.Label(self.result_frame, bg=COLOR, width=WIDGET_WIDTH-15, text='', borderwidth=2, relief="groove")
        self.event_label_res.grid(row=2, column=1)
        self.event_label_res1 = tk.Label(self.result_frame, bg=COLOR, width=WIDGET_WIDTH - 15, text='', borderwidth=2, relief="groove")
        self.event_label_res1.grid(row=2, column=2)
        self.event_label_res2 = tk.Label(self.result_frame, bg=COLOR, width=WIDGET_WIDTH - 15, text='', borderwidth=2, relief="groove")
        self.event_label_res2.grid(row=2, column=3)
        self.calculate_result_btn.grid(row=8, column=0, columnspan=2, pady=5)

    @staticmethod
    def defocus(event):
        event.widget.master.focus_set()

    def make_view(self):
        self.frame.pack(pady=10)
        self.result_frame.pack()

    def solve(self):
        a, b = int(self.a_.get()), int(self.b_.get())
        generator = EvenDistribution(a, b)
        lambda_ = int(self.lambda_.get())
        processor = NormalDistribution(lambda_)
        total_tasks = int(self.request_size.get())
        repeat_percentage = int(self.repeat_size.get())
        step = 0.1
        step_data = step_model(generator, processor, total_tasks, repeat_percentage, step)
        event_data = event_model(generator, processor, total_tasks, repeat_percentage)
        self.step_label_res['text'] = str(step_data[0])
        self.event_label_res['text'] = str(event_data[0])
        self.step_label_res1['text'] = str(step_data[1])
        self.event_label_res1['text'] = str(event_data[1])
        self.step_label_res2['text'] = str(step_data[2])
        self.event_label_res2['text'] = str(event_data[2])


root = tk.Tk()
root['bg'] = COLOR
root.geometry('620x330')
first_block = Block(root)
first_block.make_view()
root.mainloop()
