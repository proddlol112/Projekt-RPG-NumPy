
import numpy as np
import csv


# ==========================================
# DANE POSTACI
# ==========================================

nazwy = np.array([
    "Wojownik",
    "Mag",
    "Łucznik",
    "Paladyn",
    "Łotrzyk",
    "Berserker",
    "Druid",
    "Strażnik"
])

# Kolejność: HP, atak, obrona, szybkość
statystyki = np.array([
    [120, 28, 18, 9],
    [75, 44, 6, 13],
    [95, 34, 10, 17],
    [140, 25, 22, 7],
    [80, 39, 8, 21],
    [110, 42, 7, 12],
    [105, 26, 15, 14],
    [155, 18, 26, 5]
], dtype=float)

# Wagi: HP, atak, obrona, szybkość
wagi = np.array([0.20, 0.40, 0.25, 0.15])


# ==========================================
# WALIDACJA DANYCH
# ==========================================

def walidacja(nazwy, statystyki):

    if statystyki.ndim != 2 or statystyki.shape[1] != 4:
        raise ValueError("Statystyki muszą mieć dokładnie 4 kolumny.")

    if statystyki.shape[0] != len(nazwy):
        raise ValueError("Liczba wierszy musi odpowiadać liczbie nazw.")

    if len(nazwy) < 2:
        raise ValueError("Program wymaga co najmniej dwóch postaci.")

    if len(np.unique(nazwy)) != len(nazwy):
        raise ValueError("Nazwy postaci muszą być unikatowe.")

    if not np.all(np.isfinite(statystyki)):
        raise ValueError("Statystyki muszą być skończonymi liczbami.")

    if np.any(statystyki < 0):
        raise ValueError("Statystyki nie mogą być ujemne.")


# ==========================================
# NORMALIZACJA MIN-MAX
# ==========================================

def normalizacja(statystyki):

    minimum = np.min(statystyki, axis=0)
    maksimum = np.max(statystyki, axis=0)

    rozstep = maksimum - minimum

    return np.divide(
        statystyki - minimum,
        rozstep,
        out=np.zeros_like(statystyki, dtype=float),
        where=rozstep != 0
    )


# ==========================================
# OBLICZANIE SIŁY
# ==========================================

def oblicz_sile(statystyki_norm, wagi):

    return statystyki_norm @ wagi


# ==========================================
# PRZYPISYWANIE RÓL
# ==========================================

def przypisz_role(statystyki):

    warunki = [
        (statystyki[:, 1] >= 35) &
        (statystyki[:, 3] >= 12),

        (statystyki[:, 0] >= 120) &
        (statystyki[:, 2] >= 18)
    ]

    return np.select(
        warunki,
        ["Szturmowiec", "Obrońca"],
        default="Wszechstronny"
    )


# ==========================================
# MACIERZ POJEDYNKÓW
# ==========================================

def macierz_pojedynkow(sily):

    roznice = sily[:, np.newaxis] - sily[np.newaxis, :]

    macierz = 1 / (1 + np.exp(-8 * roznice))

    np.fill_diagonal(macierz, 0.5)

    return macierz


# ==========================================
# TESTY AUTOMATYCZNE
# ==========================================

def testy():

    # Test normalizacji
    dane = np.array([
        [10, 5, 2, 8],
        [20, 5, 4, 8],
        [30, 5, 6, 8]
    ], dtype=float)

    norm = normalizacja(dane)

    assert np.allclose(norm[:, 0], [0, 0.5, 1])
    assert np.allclose(norm[:, 1], [0, 0, 0])
    assert np.allclose(norm[:, 2], [0, 0.5, 1])
    assert np.allclose(norm[:, 3], [0, 0, 0])

    # Test stałych kolumn
    stale = np.array([
        [5, 10, 15, 20],
        [5, 10, 15, 20]
    ], dtype=float)

    assert np.allclose(normalizacja(stale), 0)

    # Test macierzy pojedynków
    przykladowe_sily = np.array([0.2, 0.5, 0.8])

    macierz = macierz_pojedynkow(przykladowe_sily)

    assert np.allclose(np.diag(macierz), 0.5)

    assert np.allclose(
        macierz + macierz.T,
        np.ones_like(macierz)
    )

    print("Wszystkie testy zakończone poprawnie!")


# ==========================================
# EKSPORT RANKINGU DO CSV
# ==========================================

def eksport_csv(nazwy, role, sily, szanse, ranking):

    with open(
        "raport_postaci.csv",
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as plik:

        writer = csv.writer(plik, delimiter=";")

        writer.writerow([
            "Miejsce",
            "Postać",
            "Rola",
            "Siła",
            "Średnia szansa wygranej"
        ])

        for miejsce, indeks in enumerate(ranking, start=1):

            writer.writerow([
                miejsce,
                nazwy[indeks],
                role[indeks],
                f"{sily[indeks]:.4f}",
                f"{szanse[indeks] * 100:.2f}%"
            ])


# ==========================================
# GŁÓWNA FUNKCJA PROGRAMU
# ==========================================

def main():

    # Walidacja
    walidacja(nazwy, statystyki)

    # Testy
    testy()

    # Normalizacja
    statystyki_norm = normalizacja(statystyki)

    # Obliczanie siły
    sily = oblicz_sile(statystyki_norm, wagi)

    # Role
    role = przypisz_role(statystyki)

    # Ranking stabilny
    ranking = np.argsort(-sily, kind="stable")

    print("\n=== RANKING POSTACI ===")

    for miejsce, indeks in enumerate(ranking, start=1):
        print(
            f"{miejsce}. {nazwy[indeks]} | "
            f"Siła: {sily[indeks]:.4f} | "
            f"Rola: {role[indeks]}"
        )

    # Najsilniejsza postać
    najlepszy = ranking[0]

    print("\nNajsilniejsza postać:", nazwy[najlepszy])

    # Średnia siła
    print("Średnia siła:", round(np.mean(sily), 4))

    # Filtrowanie postaci
    warunek = (
        (statystyki[:, 0] >= 100) &
        (statystyki[:, 3] >= 10) &
        (sily >= 0.45)
    )

    print("\n=== WYBRANE POSTACIE ===")
    print(nazwy[warunek])

    # Statystyki grupy
    print("\n=== STATYSTYKI GRUPY ===")
    print("Minimum:", np.min(statystyki, axis=0))
    print("Średnia:", np.mean(statystyki, axis=0))
    print("Maksimum:", np.max(statystyki, axis=0))

    # Macierz pojedynków
    pojedynki = macierz_pojedynkow(sily)

    print("\n=== MACIERZ POJEDYNKÓW ===")
    print(np.round(pojedynki, 3))

    # Średnia szansa wygranej bez pojedynku z samym sobą
    szanse = (
        np.sum(pojedynki, axis=1) - 0.5
    ) / (len(nazwy) - 1)

    print("\n=== ŚREDNIA SZANSA WYGRANEJ ===")

    for i, nazwa in enumerate(nazwy):
        print(f"{nazwa}: {szanse[i] * 100:.2f}%")

    # Sprawdzenie symetrii
    symetryczna = np.allclose(
        pojedynki + pojedynki.T,
        np.ones_like(pojedynki)
    )

    print("\n=== SPRAWDZENIE SYMETRII ===")
    print("Macierz spełnia warunek:", symetryczna)

    # Eksport CSV
    eksport_csv(
        nazwy,
        role,
        sily,
        szanse,
        ranking
    )

    print("\nRaport zapisano w pliku raport_postaci.csv")


# ==========================================
# URUCHOMIENIE
# ==========================================

if __name__ == "__main__":
    main()
