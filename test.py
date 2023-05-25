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


def calculate_intersection(p1, q1, p2, q2):
    # Funkcja pomocnicza do obliczania punktu przecięcia dwóch odcinków
    x1, y1 = p1
    x2, y2 = q1
    x3, y3 = p2
    x4, y4 = q2
    x_diff = (x1 - x2, x3 - x4)
    y_diff = (y1 - y2, y3 - y4)
    div = x_diff[0] * y_diff[1] - x_diff[1] * y_diff[0]
    if div == 0:
        return None  # Odcinki są równoległe
    d = (x1 * y2 - y1 * x2, x3 * y4 - y3 * x4)
    x = (d[0] * x_diff[1] - x_diff[0] * d[1]) / div
    y = (d[0] * y_diff[1] - y_diff[0] * d[1]) / div
    return x, y


def find_overlap(p1, q1, p2, q2):
    # Funkcja pomocnicza do znalezienia punktu przecięcia w przypadku pokrywających się odcinków
    if p1 == p2 or p1 == q2:
        return p1
    if q1 == p2 or q1 == q2:
        return q1


def intersect(p1, q1, p2, q2):
    # Funkcja główna wyznaczająca przecięcie dwóch odcinków
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        # Odcinki przecinają się
        return calculate_intersection(p1, q1, p2, q2)

    if o1 == 0 and on_segment(p1, p2, q1):
        # Odcinek p1-q1 jest współliniowy i częściowo na odcinku p2-q2
        return find_overlap(p1, q1, p2, q2)

    if o2 == 0 and on_segment(p1, q2, q1):
        # Odcinek p1-q1 jest współliniowy i częściowo na odcinku p2-q2
        return find_overlap(p1, q1, p2, q2)

    if o3 == 0 and on_segment(p2, p1, q2):
        # Odcinek p2-q2 jest współliniowy i częściowo na odcinku p1-q1
        return find_overlap(p1, q1, p2, q2)

    if o4 == 0 and on_segment(p2, q1, q2):
        # Odcinek p2-q2 jest współliniowy i częściowo na odcinku p1-q1
        return find_overlap(p1, q1, p2, q2)

    # Odcinki się nie przecinają
    return False


def plot_segments(p1, q1, p2, q2, intersection):
    # Funkcja do rysowania odcinków i punktu przecięcia w GUI
    fig, ax = plt.subplots()
    ax.plot([p1[0], q1[0]], [p1[1], q1[1]], 'b', label='Segment 1')
    ax.plot([p2[0], q2[0]], [p2[1], q2[1]], 'g', label='Segment 2')
    if intersection:
        ax.plot(intersection[0], intersection[1], 'ro', label='Intersection')
    ax.legend()
    ax.set_xlim(min(p1[0], q1[0], p2[0], q2[0]) - 1, max(p1[0], q1[0], p2[0], q2[0]) + 1)
    ax.set_ylim(min(p1[1], q1[1], p2[1], q2[1]) - 1, max(p1[1], q1[1], p2[1], q2[1]) + 1)

    # Konwersja wykresu na obiekt Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()


def find_intersection():
    # Funkcja wywoływana po naciśnięciu przycisku
    p1 = (int(entry_p1_x.get()), int(entry_p1_y.get()))
    q1 = (int(entry_q1_x.get()), int(entry_q1_y.get()))
    p2 = (int(entry_p2_x.get()), int(entry_p2_y.get()))
    q2 = (int(entry_q2_x.get()), int(entry_q2_y.get()))

    intersection = intersect(p1, q1, p2, q2)
    if intersection:
        label_result.config(text=f"Przecięcie: {intersection}")
    else:
        label_result.config(text="Odcinki się nie przecinają")

    plot_segments(p1, q1, p2, q2, intersection)


# Tworzenie okna głównego
root = tk.Tk()
root.title("Przecięcie odcinków")

# Tworzenie etykiet
label_p1 = tk.Label(root, text="Punkt P1:")
label_q1 = tk.Label(root, text="Punkt Q1:")
label_p2 = tk.Label(root, text="Punkt P2:")
label_q2 = tk.Label(root, text="Punkt Q2:")
label_result = tk.Label(root, text="")

# Tworzenie pól tekstowych
entry_p1_x = tk.Entry(root, width=5)
entry_p1_y = tk.Entry(root, width=5)
entry_q1_x = tk.Entry(root, width=5)
entry_q1_y = tk.Entry(root, width=5)
entry_p2_x = tk.Entry(root, width=5)
entry_p2_y = tk.Entry(root, width=5)
entry_q2_x = tk.Entry(root, width=5)
entry_q2_y = tk.Entry(root, width=5)

# Tworzenie przycisku
button_calculate = tk.Button(root, text="Oblicz", command=find_intersection)

# Wyśrodkowanie widgetów
root.grid_columnconfigure(1, weight=1)

# Umieszczanie widgetów w siatce
label_p1.grid(row=0, column=0, sticky="E")
entry_p1_x.grid(row=0, column=1, padx=5, pady=5)
entry_p1_y.grid(row=0, column=2, padx=5, pady=5)

label_q1.grid(row=1, column=0, sticky="E")
entry_q1_x.grid(row=1, column=1, padx=5, pady=5)
entry_q1_y.grid(row=1, column=2, padx=5, pady=5)

label_p2.grid(row=2, column=0, sticky="E")
entry_p2_x.grid(row=2, column=1, padx=5, pady=5)
entry_p2_y.grid(row=2, column=2, padx=5, pady=5)

label_q2.grid(row=3, column=0, sticky="E")
entry_q2_x.grid(row=3, column=1, padx=5, pady=5)
entry_q2_y.grid(row=3, column=2, padx=5, pady=5)

button_calculate.grid(row=4, column=0, columnspan=3, pady=10)

label_result.grid(row=5, column=0, columnspan=3)

# Uruchomienie głównej pętli programu
root.mainloop()
