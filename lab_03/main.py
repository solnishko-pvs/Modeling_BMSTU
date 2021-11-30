import tkinter as tk
from scipy.stats import chi2, chisquare

COLOR = '#dddddd'
COLUMNS_COLOR = '#ffffff'
MAX_SIZE = 10
WIDGET_WIDTH = 25

class LinearCongruent:
    m = 2**32
    a = 1664525
    c = 1013904223
    _cur = 1

    def next(self):
        self._cur = (self.a * self._cur + self.c) % self.m
        return self._cur

def khi_krit(arr):
    min_ = min(arr)
    cnt = [0 for _ in range(max(arr) - min_ + 1)]
    for elem in arr:
        cnt[elem-min_] += 1

    n = sum(cnt)
    k = len(cnt)

    p = 1 / k

    chisq = 0
    for j in range(k):
        chisq += cnt[j]**2 / p
    chisq = chisq / n - n
    #print(chisquare(cnt))
    return (1 - chi2.cdf(chisq, k)) * 100


def get_10_nums(arr, num):
    cnt = 0
    res = []
    i = 0
    while cnt != 10:
        if arr[i] > num:
            res.append(arr[i])
            cnt += 1
        i += 1
    return res


class file_nums:
    def __init__(self):
        self.nums = None
        with open('nums.txt', 'r') as f:
            nums = [list(i.split()) for i in list(f.read().split('\n'))]
            self.columns = len(nums)
            self.rows = len(nums[0])
            self.nums = [[] for _ in range(self.rows)]

            for i in range(self.columns):
                for j in range(self.rows):
                    self.nums[j].append(nums[i][j])

            self.cur_x = 0
            self.cur_y = 0

    def next(self):
        self.cur_x += 1
        if self.cur_x == self.columns:
            self.cur_x = 0
            self.cur_y += 1
        if self.cur_y == self.rows:
            self.cur_y = 0

        return self.nums[self.cur_y][self.cur_x]


class Block:
    def __init__(self, master):
        self.frame = tk.LabelFrame(master, bg=COLOR, text='Ввод данных', width=480, height=110)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.grid_propagate(False)

        self.label_input = tk.Label(self.frame, text='Ваши числа: ', bg=COLOR)
        self.entry_numbers = tk.Entry(self.frame, width=WIDGET_WIDTH+10)
        self.calculate_custom_result_btn = tk.Button(self.frame, text="Статистика хи-квадрат ваших чисел: ", width=WIDGET_WIDTH+6,
                                                     bg=COLOR,
                                                     command=self.user_solve)
        self.label_result = tk.Label(self.frame, text='', bg=COLOR)
        self.calculate_result_btn = tk.Button(self.frame, text="Вычислить для 1000 чисел", width=WIDGET_WIDTH, bg=COLOR, command=self.solve)

        self.listbox_frame = tk.LabelFrame(master, text='Матрица', bg=COLOR, width=530, height=200)
        self.listbox_frame.grid_propagate(False)



        self.result_frame = tk.LabelFrame(master, bg=COLOR, text='Результат', width=510, height=270)
        self.result_frame.grid_propagate(False)

        self.table_label = tk.Label(self.result_frame, text='Табличный способ', bg=COLOR, bd=3)
        self.algorithm_label = tk.Label(self.result_frame, text='Алгоритмический способ', bg=COLOR, bd=3)

        self.one_digit_table = tk.Listbox(self.result_frame, selectmode=tk.SINGLE, width=13, bg=COLUMNS_COLOR, height=1)
        self.two_digit_table = tk.Listbox(self.result_frame, selectmode=tk.SINGLE, width=13, bg=COLUMNS_COLOR, height=1)
        self.three_digit_table = tk.Listbox(self.result_frame, selectmode=tk.SINGLE, width=13, bg=COLUMNS_COLOR, height=1)
        self.one_digit_algorithm = tk.Listbox(self.result_frame, selectmode=tk.SINGLE, width=13, bg=COLUMNS_COLOR, height=1)
        self.two_digit_algorithm = tk.Listbox(self.result_frame, selectmode=tk.SINGLE, width=13, bg=COLUMNS_COLOR, height=1)
        self.three_digit_algorithm = tk.Listbox(self.result_frame, selectmode=tk.SINGLE, width=13, bg=COLUMNS_COLOR, height=1)
        self.one_digit_table.insert(tk.END, '1 разряд')
        self.two_digit_table.insert(tk.END, '2 разряда')
        self.three_digit_table.insert(tk.END, '3 разряда')
        self.one_digit_algorithm.insert(tk.END, '1 разряд')
        self.two_digit_algorithm.insert(tk.END, '2 разряда')
        self.three_digit_algorithm.insert(tk.END, '3 разряда')

        self.label_khi = tk.Label(self.result_frame, text='% статистики хи-квадрат', bg=COLOR, bd=3)

        self.one_digit_table_khi = tk.Label(self.result_frame, text='', bg=COLOR, bd=3)
        self.two_digit_table_khi = tk.Label(self.result_frame, text='', bg=COLOR, bd=3)
        self.three_digit_table_khi = tk.Label(self.result_frame, text='', bg=COLOR, bd=3)
        self.one_digit_algorithm_khi = tk.Label(self.result_frame, text='', bg=COLOR, bd=3)
        self.two_digit_algorithm_khi = tk.Label(self.result_frame, text='', bg=COLOR, bd=3)
        self.three_digit_algorithm_khi = tk.Label(self.result_frame, text='', bg=COLOR, bd=3)

        self.table_label.grid(row=0, column=0, columnspan=3)
        self.algorithm_label.grid(row=0, column=3, columnspan=3)

        self.one_digit_table.grid(row=1, column=0, padx=1)
        self.two_digit_table.grid(row=1, column=1, padx=1)
        self.three_digit_table.grid(row=1, column=2, padx=1)
        self.one_digit_algorithm.grid(row=1, column=3, padx=1)
        self.two_digit_algorithm.grid(row=1, column=4, padx=1)
        self.three_digit_algorithm.grid(row=1, column=5, padx=1)
        self.one_digit_table_khi.grid(row=3, column=0, padx=1)
        self.two_digit_table_khi.grid(row=3, column=1, padx=1)
        self.three_digit_table_khi.grid(row=3, column=2, padx=1)
        self.one_digit_algorithm_khi.grid(row=3, column=3, padx=1)
        self.two_digit_algorithm_khi.grid(row=3, column=4, padx=1)
        self.three_digit_algorithm_khi.grid(row=3, column=5, padx=1)
        self.label_khi.grid(row=2, column=0, columnspan=6)

        self.label_input.grid(row=0, column=0)
        self.entry_numbers.grid(row=0, column=1, padx=10)
        self.calculate_custom_result_btn.grid(row=1, column=0, pady=4)
        self.label_result.grid(row=1, column=1)
        self.calculate_result_btn.grid(row=2, column=0, columnspan=2, pady=2)

        self.data = None
        self.size = None
        self.table_gen = file_nums()
        self.listbox_list = [tk.Listbox(self.listbox_frame, selectmode=tk.SINGLE, width=8, bg=COLOR) for _ in range(MAX_SIZE)]

    def defocus(self, event):
        event.widget.master.focus_set()

    def make_view(self):
        self.frame.pack()
        #self.listbox_frame.pack()
        self.result_frame.pack()

    def fill_data(self, size):
        for i in range(size):
            for j in range(size):
                self.listbox_list[i].insert(tk.END, self.data[j, i])


    def user_solve(self):
        inp = self.entry_numbers.get()
        try:
            x = list(map(int, inp.split()))
            self.label_result['text'] = str(round(khi_krit(x), 4)) + '%'
        except:
            self.label_result['text'] = 'Ошибка ввода!!!'


    def solve(self):
        alg_arrs = [[int(generator.next()) % j for _ in range(1000)] for j in [10, 100, 1000]]

        table_arrs = [[int(self.table_gen.next()[:j]) for _ in range(1000)] for j in [1, 2, 3]]
        self.one_digit_algorithm.delete(1, tk.END)
        self.two_digit_algorithm.delete(1, tk.END)
        self.three_digit_algorithm.delete(1, tk.END)
        self.one_digit_algorithm['height'] = 11
        self.two_digit_algorithm['height'] = 11
        self.three_digit_algorithm['height'] = 11

        self.one_digit_table.delete(1, tk.END)
        self.two_digit_table.delete(1, tk.END)
        self.three_digit_table.delete(1, tk.END)
        self.one_digit_table['height'] = 11
        self.two_digit_table['height'] = 11
        self.three_digit_table['height'] = 11

        [self.one_digit_algorithm.insert(tk.END, i) for i in get_10_nums(alg_arrs[0], -1)]
        [self.two_digit_algorithm.insert(tk.END, i) for i in get_10_nums(alg_arrs[1], 9)]
        [self.three_digit_algorithm.insert(tk.END, i) for i in get_10_nums(alg_arrs[2], 99)]
        [self.one_digit_table.insert(tk.END, i) for i in get_10_nums(table_arrs[0], -1)]
        [self.two_digit_table.insert(tk.END, i) for i in get_10_nums(table_arrs[1], 9)]
        [self.three_digit_table.insert(tk.END, i) for i in get_10_nums(table_arrs[2], 99)]

        self.one_digit_algorithm_khi['text'] = str(round(khi_krit(alg_arrs[0]), 4)) + '%'
        self.two_digit_algorithm_khi['text'] = str(round(khi_krit(alg_arrs[1]), 4)) + '%'
        self.three_digit_algorithm_khi['text'] = str(round(khi_krit(alg_arrs[2]), 4)) + '%'
        self.one_digit_table_khi['text'] = str(round(khi_krit(table_arrs[0]), 4)) + '%'
        self.two_digit_table_khi['text'] = str(round(khi_krit(table_arrs[1]), 4)) + '%'
        self.three_digit_table_khi['text'] = str(round(khi_krit(table_arrs[2]), 4)) + '%'


generator = LinearCongruent()

root = tk.Tk()
root['bg'] = COLOR
root.geometry('540x390')

first_block = Block(root)
first_block.make_view()

root.mainloop()
