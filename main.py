import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def orientation(p, q, r):
    # Funkcja pomocnicza do określenia orientacji punktów p, q, r
    # Zwraca wartość dodatnią, jeśli p-q-r są ułożone w kierunku przeciwnym do ruchu wskazówek zegara,
    # wartość ujemną, jeśli p-q-r są ułożone zgodnie z ruchem wskazówek zegara,
    # wartość zero, jeśli punkty są współliniowe.
    return (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])


def on_segment(p, q, r):
    # Funkcja pomocnicza sprawdzająca, czy punkt q leży na odcinku p-r
    return min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and min(p[1], r[1]) <= q[1] <= max(p[1], r[1])


def intersect(p1, q1, p2, q2):
    # Funkcja główna wyznaczająca przecięcie dwóch odcinków
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # Sprawdzanie przypadków, w których odcinki się przecinają
    if (o1 > 0 and o2 < 0 or o1 < 0 and o2 > 0) and (o3 > 0 and o4 < 0 or o3 < 0 and o4 > 0):
        intersection = calculate_intersection(p1, q1, p2, q2)
        if intersection is not None:
            return True, intersection

    # Przypadek równoległych odcinków
    if o1 == 0 and o2 == 0 and o3 == 0 and o4 == 0:
        # Sprawdzanie pokrywania się odcinków
        if on_segment(p1, p2, q1) or on_segment(p1, q2, q1) or on_segment(p2, p1, q2) or on_segment(p2, q1, q2):
            return True, "Odcinki pokrywają się"

    return False, None



def calculate_intersection(p1, q1, p2, q2):
    # Obliczanie punktu przecięcia dwóch odcinków
    x_diff = (p1[0] - q1[0], p2[0] - q2[0])
    y_diff = (p1[1] - q1[1], p2[1] - q2[1])

    div = x_diff[0] * y_diff[1] - x_diff[1] * y_diff[0]
    if div == 0:
        return None  # Odcinki są równoległe

    d = (p1[0] * q1[1] - p1[1] * q1[0], p2[0] * q2[1] - p2[1] * q2[0])
    x = (d[0] * x_diff[1] - d[1] * x_diff[0]) / div
    y = (d[0] * y_diff[1] - d[1] * y_diff[0]) / div

    return x, y



def check_intersection():
    # Pobieranie współrzędnych odcinków z pól tekstowych
    p1_x = float(entry_p1_x.get())
    p1_y = float(entry_p1_y.get())
    q1_x = float(entry_q1_x.get())
    q1_y = float(entry_q1_y.get())
    p2_x = float(entry_p2_x.get())
    p2_y = float(entry_p2_y.get())
    q2_x = float(entry_q2_x.get())
    q2_y = float(entry_q2_y.get())

    # Wywołanie funkcji intersect i wyświetlenie wyników
    intersecting, intersection = intersect((p1_x, p1_y), (q1_x, q1_y), (p2_x, p2_y), (q2_x, q2_y))

    if intersecting:
        if isinstance(intersection, tuple):
            if intersection[0] != intersection[1]:
                result_label.config(text="Odcinki przecinają się.")
                intersection_label.config(text="Przecięcie to odcinek o końcach: {}".format(intersection))
            else:
                if (p1_x, p1_y) == intersection or (q1_x, q1_y) == intersection or (p2_x, p2_y) == intersection or (q2_x, q2_y) == intersection:
                    result_label.config(text="Odcinki przecinają się w końcu odcinka.")
                    intersection_label.config(text="Przecięcie to punkt o współrzędnych: {}".format(intersection))
                else:
                    result_label.config(text="Odcinki przecinają się wewnątrz.")
                    intersection_label.config(text="Przecięcie to punkt o współrzędnych: {}".format(intersection))
        else:
            result_label.config(text="Odcinki przecinają się.")
            intersection_label.config(text="Przecięcie to punkt o współrzędnych: {}".format(intersection))
        # Wykres z odcinkami
        fig, ax = plt.subplots()
        ax.plot([p1_x, q1_x], [p1_y, q1_y], 'b', label='Odcinek 1')
        ax.plot([p2_x, q2_x], [p2_y, q2_y], 'g', label='Odcinek 2')

        # Dodanie układu współrzędnych
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)

        # Skala osi
        ax.set_aspect('equal', adjustable='box')

        # Legenda
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        graph_frame.pack()
    else:
        result_label.config(text="Odcinki nie przecinają się.")
        intersection_label.config(text="")
        graph_frame.pack_forget()  # Ukrycie wykresu



# Tworzenie interfejsu Tkinter
root = tk.Tk()
root.title("Przecięcie odcinków")

# Ramka do wprowadzania danych
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

label_p1 = tk.Label(input_frame, text="Odcinek 1 - P:")
label_p1.grid(row=0, column=0, padx=5)
entry_p1_x = tk.Entry(input_frame, width=5)
entry_p1_x.grid(row=0, column=1, padx=5)
entry_p1_y = tk.Entry(input_frame, width=5)
entry_p1_y.grid(row=0, column=2, padx=5)

label_q1 = tk.Label(input_frame, text="Q:")
label_q1.grid(row=0, column=3, padx=5)
entry_q1_x = tk.Entry(input_frame, width=5)
entry_q1_x.grid(row=0, column=4, padx=5)
entry_q1_y = tk.Entry(input_frame, width=5)
entry_q1_y.grid(row=0, column=5, padx=5)

label_p2 = tk.Label(input_frame, text="Odcinek 2 - P:")
label_p2.grid(row=1, column=0, padx=5)
entry_p2_x = tk.Entry(input_frame, width=5)
entry_p2_x.grid(row=1, column=1, padx=5)
entry_p2_y = tk.Entry(input_frame, width=5)
entry_p2_y.grid(row=1, column=2, padx=5)

label_q2 = tk.Label(input_frame, text="Q:")
label_q2.grid(row=1, column=3, padx=5)
entry_q2_x = tk.Entry(input_frame, width=5)
entry_q2_x.grid(row=1, column=4, padx=5)
entry_q2_y = tk.Entry(input_frame, width=5)
entry_q2_y.grid(row=1, column=5, padx=5)

# Przycisk sprawdzający przecięcie
check_button = tk.Button(root, text="Sprawdź przecięcie", command=check_intersection)
check_button.pack(pady=10)

# Ramka z wynikami
result_frame = tk.Frame(root)
result_frame.pack()

result_label = tk.Label(result_frame, text="")
result_label.pack()

intersection_label = tk.Label(result_frame, text="")
intersection_label.pack()

# Ramka na wykres
graph_frame = tk.Frame(root)

root.mainloop()

