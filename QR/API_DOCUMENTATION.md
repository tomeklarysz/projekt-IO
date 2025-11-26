# QR Module - Dokumentacja

## Przegląd
Moduł QR zapewnia funkcjonalność generowania i skanowania kodów QR. Obecnie używa lokalnej bazy SQLite do testów, ale został zaprojektowany tak, aby łatwo podpiąć go do większej bazy danych projektu.

---

## Struktura Plików

```
QR/
├── generator.py     # Generowanie kodów QR
├── scanner.py       # Skanowanie kodów QR za pomocą kamery
├── remover.py       # Usuwanie kodów QR (przez skanowanie)
├── database.py      # [TYMCZASOWE] Lokalna baza SQLite do testów
├── main.py          # Interfejs CLI do testowania
└── qr_codes.db      # [TYMCZASOWE] Baza testowa
```

---

## Główne Funkcje Modułu

### 1. generator.py - Generowanie Kodów QR

#### `generate_qr_code()`
**Opis:** Generuje nowy unikalny identyfikator UUID, zapisuje go do bazy danych i tworzy obraz kodu QR.

**Parametry:** Brak

**Zwraca:**
- `filename` (str) - Nazwa pliku wygenerowanego obrazu (format: `qr_<uuid>.png`)
- `None` - Jeśli zapis do bazy danych się nie powiódł

**Skutki:**
- Tworzy plik PNG z kodem QR w bieżącym katalogu
- Zapisuje UUID do bazy danych (obecnie SQLite, później do głównej bazy)
- Wyświetla komunikaty w konsoli

**Przykład użycia:**
```python
import generator

filename = generator.generate_qr_code()
if filename:
    print(f"Kod QR zapisany jako: {filename}")
    # filename zawiera nazwę pliku, np. "qr_53b4cd8d-31f1-4e34-a7d1-35f831fb2662.png"
else:
    print("Błąd generowania kodu")
```

**Parametry kodu QR:**
- `version=1` - Rozmiar kodu QR (1 = najmniejszy)
- `error_correction=ERROR_CORRECT_L` - Niski poziom korekcji błędów
- `box_size=10` - Rozmiar każdego "pudełka" w pikselach
- `border=4` - Szerokość obramowania

---

### 2. scanner.py - Skanowanie Kodów QR

#### `scan_qr_code()`
**Opis:** Otwiera kamerę, skanuje kod QR i weryfikuje go w bazie danych.

**Parametry:** Brak

**Zwraca:** Brak (funkcja działa do momentu wykrycia kodu lub naciśnięcia 'q')

**Zachowanie:**
1. Otwiera kamerę (VideoCapture(0))
2. Wyświetla podgląd kamery w oknie "QR Code Scanner"
3. Ciągle skanuje w poszukiwaniu kodu QR
4. Po wykryciu kodu:
   - Weryfikuje kod w bazie danych
   - Jeśli kod istnieje: wyświetla "SUCCESS" i kończy
   - Jeśli kod nie istnieje: wyświetla "PERMISSION DENIED" i kontynuuje skanowanie
5. Użytkownik może nacisnąć 'q', aby zakończyć

**Przykład użycia:**
```python
import scanner

# Blokująca funkcja - zatrzyma wykonanie do momentu zeskanowania kodu
scanner.scan_qr_code()
```

---

### 3. remover.py - Usuwanie Kodów QR

#### `remove_qr_code()`
**Opis:** Otwiera kamerę, skanuje kod QR i usuwa go z bazy danych jeśli istnieje.

**Parametry:** Brak

**Zwraca:** Brak (funkcja działa do momentu wykrycia i usunięcia kodu lub naciśnięcia 'q')

**Zachowanie:**
1. Otwiera kamerę (VideoCapture(0))
2. Wyświetla podgląd kamery w oknie "QR Code Remover"
3. Ciągle skanuje w poszukiwaniu kodu QR
4. Po wykryciu kodu:
   - Jeśli kod istnieje: usuwa go i wyświetla "SUCCESS"
   - Jeśli kod nie istnieje: wyświetla komunikat i kontynuuje skanowanie
5. Użytkownik może nacisnąć 'q', aby zakończyć

**Przykład użycia:**
```python
import remover

remover.remove_qr_code()
```

---

## Integracja z Główną Bazą Danych

Obecnie moduł używa `database.py` z lokalną bazą SQLite do testów. Aby podpiąć moduł do głównej bazy danych projektu, wystarczy zastąpić wywołania funkcji z `database.py` innymi funkcjami.

Funkcje do Zastąpienia:

Moduł QR używa 4 funkcji z `database.py`:

#### 1. `database.init_db()`
**Gdzie używane:** generator.py, scanner.py, remover.py  
**Co robi:** Inicjalizuje bazę danych  
Do usunięcia w dalszej części produkcji

#### 2. `database.save_code(code_id)`
**Gdzie używane:** generator.py  
**Co robi:** Zapisuje UUID kodu QR do bazy  
**Parametry:** `code_id` (str) - UUID do zapisania  
**Zwraca:** `True` jeśli sukces, `False` jeśli błąd  

#### 3. `database.verify_code(code_id)`
**Gdzie używane:** scanner.py, remover.py  
**Co robi:** Sprawdza czy kod istnieje w bazie  
**Parametry:** `code_id` (str) - UUID do weryfikacji  
**Zwraca:** `True` jeśli kod istnieje, `False` jeśli nie  

#### 4. `database.delete_code(code_id)`
**Gdzie używane:** remover.py  
**Co robi:** Usuwa kod z bazy  
**Parametry:** `code_id` (str) - UUID do usunięcia  
**Zwraca:** `True` jeśli usunięto, `False` jeśli nie istniał  

---


## Zależności

```
qrcode==7.4.2
opencv-python==4.8.1.78
pillow==10.1.0
```

Instalacja:
```bash
pip install -r requirements.txt
```

---

### Uwagi:
- Funkcje skanujące są **blokujące** - powinny być uruchamiane w wątkach
- Obrazy QR są zapisywane w bieżącym katalogu
- UUID kodów QR to standardowe UUID v4 (36 znaków)
