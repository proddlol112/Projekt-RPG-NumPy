# Weryfikacja projektu RPG

## Tabela wymagań i wyników

| Wymaganie | Status | Dowód lub wynik testu |
|---|---|---|
| Dane postaci w tablicach NumPy | Działa | Tablice `nazwy` i `statystyki` |
| Wagi statystyk | Działa | `[0.20, 0.40, 0.25, 0.15]` |
| Normalizacja min-max | Działa | Wyniki siły od 0.395 do 0.535 |
| Obsługa stałych kolumn | Działa | Test normalizacji stałej kolumny |
| Ważony wynik siły | Działa | Obliczenia przez `normalizowana_macierz @ wagi` |
| Ranking malejący | Działa | Berserker zajmuje 1. miejsce |
| Przypisywanie ról | Działa | Wyświetlono role wszystkich 8 postaci |
| Filtrowanie postaci | Działa | Wynik: Berserker |
| Statystyki grupowe | Działa | Wyświetlono minimum, średnią i maksimum |
| Macierz pojedynków | Działa | Przekątna ma wartość 0.5, a suma elementów symetrycznych wynosi 1 |
| Średnie szanse wygranej | Działa | Berserker: 53.73% |
| Walidacja danych | Działa | Testy niepoprawnego kształtu, powtórzonych nazw, wartości ujemnych i NaN |
| Testy automatyczne | Działa | Komunikat: `Wszystkie testy zakończone poprawnie!` |
| Eksport CSV | Działa | Plik `raport_postaci.csv`, rozmiar 348 bajtów |

## Wyniki uruchomienia

- Liczba postaci: 8
- Najsilniejsza postać: Berserker
- Siła Berserkera: 0.535
- Średnia siła: 0.471
- Postać spełniająca warunki filtrowania: Berserker
- Średnia szansa wygranej Berserkera: 53.73%
- Wynik testów automatycznych: poprawny
- Eksport CSV: poprawny

## Korekty po niepełnych wynikach AI

1. Po zmianie programu na NumPy usunięto część wcześniejszych funkcji. Poprawiono prompt, aby zachować obliczanie siły, ranking, najsilniejszą postać i średnią.
2. Po dodaniu normalizacji otrzymano niepełny kod. Doprecyzowano prompt, wymagając kompletnego pliku, obsługi stałych kolumn i zachowania funkcji main().
3. Podczas sprawdzania eksportu wykryto brak zapisu CSV w używanej wersji programu. Dodano funkcję zapisu i sprawdzono ponownie działanie programu.

## Uwagi

Macierz pojedynków przedstawia szacowane prawdopodobieństwo wygranej obliczone na podstawie wartości siły postaci. Nie jest to symulacja pełnego systemu walki.