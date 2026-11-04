# Prompty – Projekt RPG

## 1. Analiza kodu początkowego
Przeanalizuj początkowy kod programu RPG. Opisz jego działanie, dane postaci, sposób obliczania siły oraz ranking. Na tym etapie nie zmieniaj kodu.

**Zmiana:** poznanie struktury programu i zaplanowanie dalszych modyfikacji.

## 2. Wykorzystanie biblioteki NumPy
Przekształć statystyki postaci w macierz NumPy. Nazwy postaci przechowuj w osobnej tablicy. Wagi statystyk przechowuj w tablicy NumPy.

**Zmiana:** zastosowanie tablic i operacji NumPy zamiast zwykłych struktur danych.

## 3. Zachowanie wcześniejszych funkcji
W poprzedniej wersji zostały usunięte niektóre wcześniejsze funkcje. Popraw kod tak, aby nadal obliczał siłę postaci, wyświetlał ranking, wskazywał najsilniejszą postać i obliczał średnią siłę.

**Zmiana:** przywrócenie wcześniejszej funkcjonalności programu.

## 4. Normalizacja i ważona siła
Dodaj normalizację min-max dla statystyk postaci. Następnie oblicz ważony wynik na podstawie wag: HP 0.20, atak 0.40, obrona 0.25 i szybkość 0.15. Zachowaj ranking malejący.

**Zmiana:** wprowadzenie normalizacji i ważonego wyniku siły.

## 5. Poprawna obsługa stałych kolumn
Popraw normalizację tak, aby prawidłowo obsługiwała kolumny, w których wszystkie wartości są takie same. Użyj np.divide z parametrami out i where, aby uniknąć dzielenia przez zero.

**Zmiana:** zabezpieczenie normalizacji przed błędem dla stałych kolumn.

## 6. Role i filtrowanie postaci
Dodaj automatyczne przypisywanie ról postaci na podstawie ich statystyk. Wykorzystaj np.select. Dodaj również filtrowanie postaci według HP, szybkości i obliczonej siły.

**Zmiana:** dodanie ról oraz filtrowania.

## 7. Statystyki grupowe
Dodaj obliczanie minimalnej, średniej i maksymalnej wartości HP, ataku, obrony oraz szybkości.

**Zmiana:** dodanie statystyk opisowych całej grupy postaci.

## 8. Macierz pojedynków
Dodaj macierz pojedynków, w której każda para postaci ma obliczone szacowane prawdopodobieństwo wygranej na podstawie ich siły. Na przekątnej macierzy ustaw wartość 0.5.

**Zmiana:** dodanie macierzy porównującej postacie.

## 9. Średnie szanse i raport CSV
Oblicz średnie szanse wygranej każdej postaci. Dodaj walidację danych, testy automatyczne oraz zapis raportu do pliku CSV. Zachowaj pełny kod programu i możliwość uruchomienia go przez funkcję main().

**Zmiana:** dodanie walidacji, testów i eksportu wyników do CSV.

## Korekty promptów

### Korekta 1
Po przejściu na NumPy część wcześniejszych funkcji została usunięta. Doprecyzowano polecenie, aby zachować obliczanie siły, ranking, wskazywanie najsilniejszej postaci i średnią siłę.

### Korekta 2
Po dodaniu normalizacji AI zwróciło niepełny kod. Polecenie zostało poprawione: wymagano kompletnego pliku, zachowania wszystkich wcześniejszych funkcji, obsługi stałych kolumn przez np.divide oraz pełnej funkcji main().

### Korekta 3
Po otrzymaniu kodu z eksportem CSV sprawdzono uruchomienie programu. Wykryto brak funkcji zapisu CSV w używanej wersji pliku. Dodano funkcję zapisz_csv() i wywołanie jej w main(). Po poprawce raport został zapisany poprawnie.