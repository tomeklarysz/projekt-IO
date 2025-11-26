# Dokumentacja Modułu `face_auth`

Moduł `face_auth` odpowiada za uwierzytelnianie użytkowników na podstawie rozpoznawania twarzy. Wykorzystuje bibliotekę `DeepFace` do generowania i porównywania wektorów cech twarzy oraz `OpenCV` do obsługi kamery i przetwarzania obrazu.

## Struktura Modułu

Moduł składa się z następujących plików:
- `admin.py`: Funkcje administracyjne do zarządzania danymi biometrycznymi pracowników.
- `authenticator.py`: Główna logika uwierzytelniania użytkownika.
- `camera.py`: Obsługa kamery internetowej.
- `recognizer.py`: Wrapper na bibliotekę `DeepFace` do rozpoznawania twarzy.

---

## 1. `admin.py`

Zawiera funkcje pomocnicze do rejestracji i aktualizacji danych biometrycznych pracowników.

### Funkcje

#### `upsert_employee_from_photo(photo_path, employee_id, first_name=None, last_name=None, qr_hash=None)`

Aktualizuje lub wstawia wektor twarzy pracownika na podstawie dostarczonego zdjęcia.

- **Parametry:**
  - `photo_path` (str): Ścieżka do pliku ze zdjęciem.
  - `employee_id` (int): ID pracownika.
  - `first_name` (str, opcjonalnie): Imię (wymagane dla nowego pracownika).
  - `last_name` (str, opcjonalnie): Nazwisko (wymagane dla nowego pracownika).
  - `qr_hash` (str, opcjonalnie): Hash QR (wymagane dla nowego pracownika).

- **Zwraca:**
  - `str`: Komunikat o wyniku operacji ("Updated", "Created", "Not Found", "Error" lub szczegóły błędu).

---

## 2. `authenticator.py`

Zawiera klasę `FaceAuthenticator`, która zarządza procesem weryfikacji tożsamości użytkownika.

### Klasa `FaceAuthenticator`

#### `__init__()`
Inicjalizuje instancję `FaceRecognizer`.

#### `ensure_user_has_vector(user_id)`
Sprawdza, czy użytkownik posiada wektor twarzy w bazie danych. Jeśli nie, próbuje go wygenerować na podstawie zapisanego zdjęcia (`photo_path`).

- **Parametry:**
  - `user_id` (int): ID użytkownika do sprawdzenia.

- **Zwraca:**
  - `(numpy_array, str)`: Krotka zawierająca wektor twarzy (jeśli sukces) lub `None`, oraz komunikat błędu (jeśli wystąpił) lub `None`.

#### `verify_user(user_id, timeout=10)`
Weryfikuje, czy osoba przed kamerą to użytkownik o podanym `user_id`. Uruchamia podgląd z kamery i porównuje twarz w czasie rzeczywistym.

- **Parametry:**
  - `user_id` (int): ID użytkownika do weryfikacji.
  - `timeout` (int, domyślnie 10): Czas w sekundach, po którym weryfikacja zostanie przerwana, jeśli nie uda się dopasować twarzy.

- **Zwraca:**
  - `(bool, str)`: Krotka `(True, "Verification successful.")` jeśli weryfikacja się powiodła, w przeciwnym razie `(False, komunikat_błędu)`.

---

## 3. `camera.py`

Obsługuje interakcję z kamerą internetową. Implementuje protokół Context Manager (`with Camera() as cam:`).

### Klasa `Camera`

#### `__init__(camera_index=0)`
Konstruktor klasy.
- **Parametry:**
  - `camera_index` (int, domyślnie 0): Indeks urządzenia kamery.

#### `start()`
Uruchamia przechwytywanie obrazu z kamery. Rzuca wyjątek `RuntimeError`, jeśli nie można otworzyć kamery.

#### `get_frame()`
Pobiera pojedynczą klatkę z kamery.
- **Zwraca:**
  - `numpy.ndarray`: Obraz klatki z kamery.

#### `stop()`
Zwalnia zasoby kamery.

---

## 4. `recognizer.py`

Wrapper na bibliotekę `DeepFace`, dostarczający uproszczony interfejs do generowania embeddingów i porównywania twarzy.

### Klasa `FaceRecognizer`

#### `__init__(model_name="Facenet")`
Inicjalizuje model DeepFace. Wykonuje próbne wywołanie, aby załadować model do pamięci.
- **Parametry:**
  - `model_name` (str, domyślnie "Facenet"): Nazwa modelu do użycia (np. "Facenet", "VGG-Face", "ArcFace").

#### `get_face_encoding(image)`
Oblicza embedding (wektor cech) dla pierwszej twarzy wykrytej na obrazie.

- **Parametry:**
  - `image` (numpy.ndarray): Obraz wejściowy (BGR, format OpenCV).

- **Zwraca:**
  - `list` lub `None`: Lista floatów reprezentująca wektor twarzy, lub `None` jeśli nie wykryto twarzy.

#### `compare_faces(known_vector, unknown_vector, threshold=0.4)`
Porównuje znany wektor twarzy z nieznanym wektorem używając podobieństwa cosinusowego.

- **Parametry:**
  - `known_vector` (list/numpy.array): Wzorcowy wektor twarzy.
  - `unknown_vector` (list/numpy.array): Wektor twarzy do sprawdzenia.
  - `threshold` (float, domyślnie 0.4): Próg akceptacji. Jeśli dystans cosinusowy jest mniejszy od progu, twarze są uznawane za zgodne.

- **Zwraca:**
  - `bool`: `True` jeśli twarze pasują, `False` w przeciwnym razie.

#### `load_image_file(path)`
Wczytuje obraz z pliku za pomocą OpenCV.

- **Parametry:**
  - `path` (str): Ścieżka do pliku obrazu.

- **Zwraca:**
  - `numpy.ndarray`: Obraz w formacie BGR.
