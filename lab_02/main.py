import tkinter as tk
from tkinter import ttk
import numpy as np
from random import randint

MINVALUE_GEN = 1
MAXVALUE_GEN = 10000
MAXVALUE_LESS = MAXVALUE_GEN  # // 10
COLOR = '#dddddd'
COLUMNS_COLOR = '#ffffff'
MAX_SIZE = 10
WIDGET_WIDTH = 15


def build_coeff_matrix(matrix):
    matrix = np.array(matrix)
    n = len(matrix)
    res = np.zeros((n, n))

    for state in range(n - 1):
        for col in range(n):
            res[state, state] -= matrix[state, col]
        for row in range(n):
            res[state, row] += matrix[row, state]

    for state in range(n):
        res[n - 1, state] = 1

    return res


def build_augmentation_matrix(count):
    res = [0 for _ in range(count)]
    res[count - 1] = 1
    return np.array(res)


def solve(matrix):
    return np.linalg.solve(build_coeff_matrix(matrix), build_augmentation_matrix(len(matrix)))


EPS = TIME_DELTA = 1e-3


def get_probability_increments(matrix, probabilities):
    n = len(matrix)
    return [TIME_DELTA * sum([probabilities[j] * (-sum(matrix[i])) if i == j
                              else probabilities[j] * matrix[j][i] for j in range(n)]) for i in range(n)]


def calc_stabilization_times(matrix, start_probabilities, limit_probabilities):
    n = len(matrix)
    current_time = 0
    current_probabilities = start_probabilities.copy()
    stabilization_times = [0] * n

    while not all(stabilization_times):
        curr_dps = get_probability_increments(matrix, current_probabilities)
        for i in range(n):
            if not stabilization_times[i] and abs(current_probabilities[i] - limit_probabilities[i]) <= EPS:
                stabilization_times[i] = current_time
            current_probabilities[i] += curr_dps[i]
        current_time += TIME_DELTA
    return stabilization_times


class Block:
    def __init__(self, master):

        self.frame = tk.LabelFrame(master, bg=COLOR, text='Ввод данных', width=530, height=110)
        self.frame.columnconfigure((0, 1), weight=1)
        self.frame.rowconfigure((0, 1), weight=1)
        self.frame.grid_propagate(False)
        # self.ent = tk.Entry(self.frame, width=20)
        self.generate_random_btn = tk.Button(self.frame, text="Заполнить", width=WIDGET_WIDTH,
                                             command=self.generate_random, bg=COLOR)
        self.fill_zero_btn = tk.Button(self.frame, text="Обнулить", width=WIDGET_WIDTH,
                                       command=self.generate_matrix, bg=COLOR)
        self.calculate_result_btn = tk.Button(self.frame, text="Вычислить", width=WIDGET_WIDTH*2+2,
                                              bg=COLOR, command=self.solve)
        self.lab = tk.Label(self.frame, bg=COLOR, width=WIDGET_WIDTH, text='Размер матрицы:')

        self.listbox_frame = tk.LabelFrame(master, text='Матрица', bg=COLOR, width=530, height=190)
        self.listbox_frame.grid_propagate(False)
        # self.listbox = tk.Listbox(self.frame, selectmode=tk.SINGLE)
        self.style = ttk.Style()
        self.style.configure('TCombobox', fieldbackground=COLUMNS_COLOR)
        self.matrix_size = ttk.Combobox(self.frame, width=WIDGET_WIDTH, values=[i for i in range(1, MAX_SIZE + 1)],
                                        state='readonly')

        self.matrix_size.bind("<FocusIn>", self.defocus)
        self.matrix_size.set(4)

        self.result_frame = tk.LabelFrame(master, bg=COLOR, text='Результат', width=530, height=200)
        self.result_frame.grid_propagate(False)
        self.res_states = tk.Listbox(self.result_frame, selectmode=tk.SINGLE, width=28, bg=COLUMNS_COLOR, height=1)
        self.res_probability = tk.Listbox(self.result_frame, selectmode=tk.SINGLE, width=28, bg=COLUMNS_COLOR, height=1)
        self.res_time = tk.Listbox(self.result_frame, selectmode=tk.SINGLE, width=28, bg=COLUMNS_COLOR, height=1)
        self.res_states.insert(tk.END, 'Состояние')
        self.res_probability.insert(tk.END, 'Предельная вероятность')
        self.res_time.insert(tk.END, 'Время')
        self.res_states.grid(row=1, column=0, padx=1)
        self.res_probability.grid(row=1, column=1, padx=2)
        self.res_time.grid(row=1, column=2, padx=1)

        self.lab.grid(row=0, column=0, padx=2, sticky=tk.E)
        self.matrix_size.grid(row=0, column=1, pady=2, padx=2, sticky=tk.W)

        self.generate_random_btn.grid(row=1, column=0, pady=2, padx=2, sticky=tk.E)
        self.fill_zero_btn.grid(row=1, column=1, pady=2, padx=2, sticky=tk.W)

        self.calculate_result_btn.grid(row=2, column=0, columnspan=2, pady=2)
        # self.listbox.grid(row=4, column=0, columnspan=10)

        self.data = None
        self.data_list = None
        self.size = None
        self.listbox_list = [tk.Listbox(self.listbox_frame, selectmode=tk.SINGLE, width=8, bg=COLUMNS_COLOR)
                             for _ in range(MAX_SIZE)]

        # self.but['command'] = getattr(self, func)

    @staticmethod
    def defocus(event):
        event.widget.master.focus_set()

    def make_view(self):
        # self.frame.grid(row=row, column=column)
        self.frame.pack()
        # self.listbox_frame.grid(row=3, column=0, columnspan=10)
        self.listbox_frame.pack()
        self.result_frame.pack()

    def generate_random(self):
        self.generate_random_btn['state'] = tk.DISABLED
        self.fill_zero_btn['state'] = tk.DISABLED
        size = int(self.matrix_size.get())
        self.size = size
        self.data_list = [[(randint(MINVALUE_GEN, MAXVALUE_GEN) / MAXVALUE_LESS)
                           if i != j else 0 for i in range(size)] for j in range(size)]
        self.data = np.matrix(self.data_list)
        self.make_listboxes(size)
        self.fill_data(size)
        self.generate_random_btn['state'] = tk.NORMAL
        self.fill_zero_btn['state'] = tk.NORMAL

    def make_listboxes(self, size):
        if self.listbox_list:
            for obj in self.listbox_list:
                obj.delete(0, tk.END)

        for i in range(size):
            self.listbox_list[i]['height'] = size
            self.listbox_list[i].grid(row=0, column=i)

        for i in range(size, MAX_SIZE):
            self.listbox_list[i].grid_remove()

    def fill_data(self, size):
        for i in range(size):
            for j in range(size):
                self.listbox_list[i].insert(tk.END, self.data[j, i])

    def generate_matrix(self):
        self.generate_random_btn['state'] = tk.DISABLED
        self.fill_zero_btn['state'] = tk.DISABLED
        size = int(self.matrix_size.get())
        self.size = size
        self.data = np.matrix([[0 for _ in range(size)] for _ in range(size)])
        self.make_listboxes(size)
        self.fill_data(size)
        self.generate_random_btn['state'] = tk.NORMAL
        self.fill_zero_btn['state'] = tk.NORMAL

    def solve(self):
        if self.size:
            # result = calculate(self.data)
            result = solve(self.data)
            self.res_states.delete(1, tk.END)
            self.res_probability.delete(1, tk.END)
            self.res_time.delete(1, tk.END)
            self.res_states['height'] = self.size + 1
            self.res_probability['height'] = self.size + 1
            self.res_time['height'] = self.size + 1
            times = calc_stabilization_times(self.data_list, list(build_augmentation_matrix(self.size)), list(result))
            for i in range(len(result)):
                self.res_states.insert(tk.END, 'STATE ' + str(i))
                self.res_probability.insert(tk.END, round(result[i], 4))
                self.res_time.insert(tk.END, round(times[i], 4))


root = tk.Tk()
root['bg'] = COLOR
root.geometry('540x510')

first_block = Block(root)
first_block.make_view()
root.mainloop()
