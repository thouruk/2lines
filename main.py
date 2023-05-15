
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
    if o1 != o2 and o3 != o4:
        return True, (p1, q1) if on_segment(p1, p2, q1) else (p1, q2)
    
    # Przypadki szczególne dla współliniowych odcinków
    if o1 == 0 and on_segment(p1, p2, q1):
        return True, (p1, q1)
    if o2 == 0 and on_segment(p1, q2, q1):
        return True, (p1, q1)
    if o3 == 0 and on_segment(p2, p1, q2):
        return True, (p2, q2)
    if o4 == 0 and on_segment(p2, q1, q2):
        return True, (p2, q2)

    return False, None

# Przykładowe dane wejściowe
p1 = (1, 1)
q1 = (4, 4)
p2 = (1, 4)
q2 = (4, 1)

# Wywołanie funkcji intersect i wyświetlenie wyników
intersecting, intersection = intersect(p1, q1, p2, q2)

if intersecting:
    print("Odcinki przecinają się.")
    if isinstance(intersection, tuple):
        print("Przecięcie to odcinek o końcach:", intersection)
    else:
        print("Przecięcie to punkt o współrzędnych:", intersection)

else:
    print("Odcinki nie przecinają się.")
