import numpy as np
import csv
from pathlib import Path


# ==========================================
# 1. DANE POSTACI
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

# Kolejność kolumn: HP, atak, obrona, szybkość
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
# 2. WALIDACJA DANYCH
# ==========================================

def waliduj_dane(nazwy_postaci, dane):
    if dane.ndim != 2 or dane.shape[1] != 4:
        raise ValueError("Macierz musi mieć dokładnie 4 kolumny.")

    if len(nazwy_postaci) != len(dane):
        raise ValueError("Liczba nazw i postaci musi być taka sama.")

    if len(nazwy_postaci) < 2:
        raise ValueError("Potrzebne są co najmniej 2 postacie.")

    if len(set(nazwy_postaci)) != len(nazwy_postaci):
        raise ValueError("Nazwy postaci nie mogą się powtarzać.")

    if not np.all(np.isfinite(dane)):
        raise ValueError("Statystyki muszą być liczbami skończonymi.")

    if np.any(dane < 0):
        raise ValueError("Statystyki nie mogą być ujemne.")

    if len(wagi) != dane.shape[1]:
        raise ValueError("Liczba wag musi odpowiadać liczbie statystyk.")

    if not np.isclose(np.sum(wagi), 1.0):
        raise ValueError("Suma wag musi wynosić 1.")

    return True


# ==========================================
# 3. NORMALIZACJA MIN-MAX
# ==========================================

def normalizuj(dane):
    minimum = np.min(dane, axis=0)
    zakres = np.ptp(dane, axis=0)

    wynik = np.zeros_like(dane, dtype=float)

    np.divide(
        dane - minimum,
        zakres,
        out=wynik,
        where=zakres != 0
    )

    return wynik


# ==========================================
# 4. OBLICZANIE SIŁY POSTACI
# ==========================================

def oblicz_sile(dane):
    normalizowana_macierz = normalizuj(dane)
    sila = normalizowana_macierz @ wagi

    return sila


# ==========================================
# 5. PRZYPISYWANIE RÓL
# ==========================================

def przypisz_role(dane):
    warunki = [
        (dane[:, 2] >= 18),
        (dane[:, 1] >= 38),
    ]

    role = [
        "Obrońca",
        "Szturmowiec"
    ]

    return np.select(
        warunki,
        role,
        default="Wszechstronny"
    )


# ==========================================
# 6. FILTROWANIE POSTACI
# ==========================================

def filtruj_postacie(dane, sila):
    warunek = (
        (dane[:, 0] >= 100) &
        (dane[:, 3] >= 10) &
        (sila >= 0.45)
    )

    return np.where(warunek)[0]


# ==========================================
# 7. STATYSTYKI GRUPOWE
# ==========================================

def oblicz_statystyki(dane):
    nazwy_statystyk = [
        "HP",
        "Atak",
        "Obrona",
        "Szybkość"
    ]

    wyniki = {}

    for i, nazwa in enumerate(nazwy_statystyk):
        wyniki[nazwa] = {
            "minimum": np.min(dane[:, i]),
            "średnia": np.mean(dane[:, i]),
            "maksimum": np.max(dane[:, i])
        }

    return wyniki


# ==========================================
# 8. MACIERZ POJEDYNKÓW
# ==========================================

def oblicz_macierz_pojedynkow(sila):
    liczba = len(sila)
    macierz = np.zeros((liczba, liczba), dtype=float)

    for i in range(liczba):
        for j in range(liczba):
            if i == j:
                macierz[i, j] = 0.5
            else:
                suma = sila[i] + sila[j]

                if suma == 0:
                    macierz[i, j] = 0.5
                else:
                    macierz[i, j] = sila[i] / suma

    return macierz


# ==========================================
# 9. ŚREDNIE SZANSE WYGRANEJ
# ==========================================

def srednie_szanse(macierz):
    liczba = macierz.shape[0]

    if liczba < 2:
        raise ValueError("Potrzebne są co najmniej 2 postacie.")

    return (
        np.sum(macierz, axis=1) - 0.5
    ) / (liczba - 1)


# ==========================================
# 10. ZAPIS RAPORTU CSV
# ==========================================

def zapisz_csv(ranking, sila, role, szanse):
    sciezka = (
        Path(__file__).resolve().parent /
        "raport_postaci.csv"
    )

    with open(
        sciezka,
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
                f"{sila[indeks]:.4f}",
                f"{szanse[indeks] * 100:.2f}%"
            ])

    print(f"\nRaport zapisano do pliku: {sciezka}")


# ==========================================
# 11. TESTY AUTOMATYCZNE
# ==========================================

def testy():
    # Test normalizacji
    dane_testowe = np.array([
        [1, 5],
        [2, 5],
        [3, 5]
    ], dtype=float)

    wynik = normalizuj(dane_testowe)

    assert np.allclose(wynik[:, 0], [0, 0.5, 1])
    assert np.allclose(wynik[:, 1], [0, 0, 0])

    # Test siły
    assert len(oblicz_sile(statystyki)) == len(nazwy)

    # Test rankingu
    sila_testowa = oblicz_sile(statystyki)
    ranking_testowy = np.argsort(-sila_testowa, kind="stable")

    assert len(ranking_testowy) == len(nazwy)
    assert sila_testowa[ranking_testowy[0]] == np.max(sila_testowa)

    # Test macierzy pojedynków
    macierz = oblicz_macierz_pojedynkow(sila_testowa)

    assert np.allclose(np.diag(macierz), 0.5)
    assert np.allclose(macierz + macierz.T, 1.0)

    # Test średnich szans
    szanse = srednie_szanse(macierz)

    assert len(szanse) == len(nazwy)
    assert np.all(np.isfinite(szanse))

    # Test walidacji
    assert waliduj_dane(nazwy, statystyki)

    # Test niepoprawnych danych
    try:
        waliduj_dane(nazwy, np.array([[1, 2, 3]]))
        assert False
    except ValueError:
        pass

    try:
        waliduj_dane(
            np.array(["A", "A"]),
            np.array([[1, 2, 3, 4], [2, 3, 4, 5]], dtype=float)
        )
        assert False
    except ValueError:
        pass

    try:
        waliduj_dane(
            np.array(["A", "B"]),
            np.array([[1, 2, 3, 4], [-1, 2, 3, 4]], dtype=float)
        )
        assert False
    except ValueError:
        pass

    try:
        waliduj_dane(
            np.array(["A", "B"]),
            np.array([[1, 2, 3, 4], [np.nan, 2, 3, 4]])
        )
        assert False
    except ValueError:
        pass

    print("\nWszystkie testy zakończone poprawnie!")


# ==========================================
# 12. FUNKCJA MAIN
# ==========================================

def main():
    waliduj_dane(nazwy, statystyki)

    sila = oblicz_sile(statystyki)
    role = przypisz_role(statystyki)

    ranking = np.argsort(-sila, kind="stable")

    macierz = oblicz_macierz_pojedynkow(sila)
    szanse = srednie_szanse(macierz)

    srednia_sila = np.mean(sila)

    # Siła postaci
    print("=" * 50)
    print("             SIŁA POSTACI RPG")
    print("=" * 50)

    for i in range(len(nazwy)):
        print(f"{nazwy[i]}: {sila[i]:.3f}")

    # Ranking
    print("\n" + "=" * 50)
    print("              RANKING POSTACI")
    print("=" * 50)

    for miejsce, indeks in enumerate(ranking, start=1):
        print(
            f"{miejsce}. {nazwy[indeks]} "
            f"- siła: {sila[indeks]:.3f}"
        )

    # Najsilniejsza postać
    indeks_najlepszej = ranking[0]

    print("\n" + "=" * 50)
    print("           NAJSILNIEJSZA POSTAĆ")
    print("=" * 50)

    print(nazwy[indeks_najlepszej])
    print(f"Siła: {sila[indeks_najlepszej]:.3f}")

    # Średnia siła
    print("\n" + "=" * 50)
    print("              ŚREDNIA SIŁA")
    print("=" * 50)

    print(f"{srednia_sila:.3f}")

    # Role
    print("\n" + "=" * 50)
    print("                ROLE POSTACI")
    print("=" * 50)

    for i in range(len(nazwy)):
        print(f"{nazwy[i]}: {role[i]}")

    # Filtrowanie
    print("\n" + "=" * 50)
    print("             FILTROWANIE POSTACI")
    print("=" * 50)

    wybrane = filtruj_postacie(statystyki, sila)

    for indeks in wybrane:
        print(nazwy[indeks])

    # Statystyki grupowe
    print("\n" + "=" * 50)
    print("             STATYSTYKI GRUPOWE")
    print("=" * 50)

    statystyki_grupy = oblicz_statystyki(statystyki)

    for nazwa, wartosci in statystyki_grupy.items():
        print(
            f"{nazwa}: minimum = {wartosci['minimum']:.2f}, "
            f"średnia = {wartosci['średnia']:.2f}, "
            f"maksimum = {wartosci['maksimum']:.2f}"
        )

    # Macierz pojedynków
    print("\n" + "=" * 50)
    print("             MACIERZ POJEDYNKÓW")
    print("=" * 50)

    print("Wiersz = postać, kolumna = przeciwnik")
    print("Wartości oznaczają szacowane prawdopodobieństwo wygranej.")

    print("       " + " ".join(f"{n[:5]:>7}" for n in nazwy))

    for i in range(len(nazwy)):
        print(
            f"{nazwy[i][:7]:>7} " +
            " ".join(f"{wartosc:7.2%}" for wartosc in macierz[i])
        )

    # Średnie szanse wygranej
    print("\n" + "=" * 50)
    print("          ŚREDNIE SZANSE WYGRANEJ")
    print("=" * 50)

    for indeks in ranking:
        print(f"{nazwy[indeks]}: {szanse[indeks]:.2%}")

    # Testy
    testy()

    # CSV
    zapisz_csv(ranking, sila, role, szanse)

    print("\n" + "=" * 50)
    print("             KONIEC PROGRAMU")
    print("=" * 50)


# ==========================================
# 13. URUCHOMIENIE PROGRAMU
# ==========================================

if __name__ == "__main__":
    main()