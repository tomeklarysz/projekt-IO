# Scenariusze Testowe

Dokument służy do przeprowadzenia testów akceptacyjnych systemu.


## Rola: Administrator

| Nr | Nazwa Przypadku | Warunki Wstępne | Kroki Testowe | Oczekiwany Rezultat | Wynik Testu |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **Dodanie nowego pracownika** | Przygotowane zdjęcie (JPG/PNG). | 1. Wejść w "Add worker".<br>2. Wypełnić formularz.<br>3. Załączyć zdjęcie.<br>4. Kliknąć "Register worker". | Komunikat sukcesu, pracownik na liście, w widoku ze szczegółami widoczne dane pracownika z formularza, wygenerowany kod QR i ID pracownika. | OK |
| 2 | **Walidacja dodawania (brak zdjęcia)** | - | 1. Spróbować dodać pracownika bez zdjęcia. | Blokada operacji | OK |
| 3 | **Aktualizacja zdjęcia pracownika - zdjęcie z widoczną twarzą** | Istniejący pracownik. | 1. Wybrać pracownika.<br>2. Zmienić zdjęcie na zdjęcie z widoczną twarzą.<br>3. Zapisać. | Zdjęcie zaktualizowane w szczegółach pracownika, kod QR nie zmienił się. | OK |
| 4 | **Aktualizacja zdjęcia pracownika - zdjęcie z niewidoczną twarzą** | Istniejący pracownik. | 1. Wybrać pracownika.<br>2. Zmienić zdjęcie na zdjęcie z niewidoczną twarzą.<br>3. Zapisać. | Blokada operacji, komunikat o błędzie. | OK |
| 5 | **Usunięcie pracownika** | Istniejący pracownik. | 1. Wybrać pracownika.<br>2. Kliknąć przycisk z ikonką kosza.<br>3. Potwierdzić. | Pracownik znika z listy, kod QR przestaje działać. | OK |
| 6 | **Pobieranie Kodu QR** | Istniejący pracownik. | 1. Wejść w szczegóły pracownika.<br>2. Kliknąć w widoczny kod QR.<br>3. Kliknąć "Download". | Pobranie pliku PNG. | OK |
| 7 | **Edycja ważności QR - ustawienie daty w przeszłości** | Istniejący pracownik. | 1. Wejść w edycję.<br>2. Zmienić datę ważności na wczorajszą.<br>3. Zapisać. | Komunikat o udanej zmianie, nowa data widoczna w szczegółach pracownika, QR przestaje działać. | OK |
| 8 | **Edycja ważności QR - ustawienie daty w przyszłości** | Istniejący pracownik. | 1. Wejść w edycję.<br>2. Zmienić datę ważności na dzień po aktualnej.<br>3. Zapisać. | Komunikat o udanej zmianie, nowa data widoczna w szczegółach pracownika, QR dalej działa. | OK |
| 9 | **Przegląd logów** | Wykonane testy 1-5 dla roli Pracownika. | 1. Wejść w "Access Logs".<br>2. Sprawdzić listę. | Lista zawiera poprawne wpisy z testów (daty, nazwiska, statusy). | OK |
| 10 | **Pobranie raportu** | Dostępne logi w bazie. | 1. Kliknąć "Pobierz raport". | Pobranie pliku z historią zdarzeń. | BŁĄD - brak możliwości pobrania raportu z interfejsu |

## Rola: Pracownik

| Nr | Nazwa Przypadku | Warunki Wstępne | Kroki Testowe | Oczekiwany Rezultat | Wynik |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **Poprawna weryfikacja tożsamości** | Pracownik zarejestrowany, ważny QR, twarz widoczna. | 1. Pokazać kod QR do kamery<br>2. Po zielonym komunikacie pokazać twarz do kamery. | Po pokazaniu kodu QR zielony komunikat: "QR ACCEPTED: <imię pracownika>". Po pokazaniu twarzy zielony komunikat "Identity Verified". | OK |
| 2 | **Błędny Kod QR (Nieznany)** | Kod QR nieistniejący w bazie. | 1. Pokazać nieznany kod QR do kamery. | Czerwony komunikat "QR Not Found", odrzucenie. | OK |
| 3 | **Przeterminowany Kod QR** | Kod QR z datą ważności w przeszłości. | 1. Pokazać przeterminowany kod QR do kamery. | Czerwony komunikat o wygaśnięciu "QR Expired", odrzucenie. | OK |
| 4 | **Brak zgodności twarzy** | Poprawny QR osoby A, przed kamerą osoba B. | 1. Pokazać poprawny kod QR.<br>2. Pokazać twarz innej osoby. | Komunikat "QR ACCEPTED: <imię pracownika>". Komunikat "VERIFICATION FAILED" po 5 sekundach, Reset procesu. | OK |
| 5 | **Brak wykrycia twarzy (Timeout)** | Poprawny QR, brak twarzy po zeskanowaniu. | 1. Pokazać poprawny kod QR.<br>2. Nie pokazywać twarzy / zasłonić ją przez 10s. | Komunikat "QR ACCEPTED: <imię pracownika>". Komunikat "VERIFICATION FAILED" po 5 sekundach, Reset procesu. | OK |