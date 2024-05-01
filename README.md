# Instrukcja Uruchomienia
Aby uruchomić ten projekt, potrzebujesz Docker'a. Poniższe kroki należy wykonać w PowerShell na systemie Windows.

### Krok 1: Klonowanie repozytorium
Skopiuj repozytorium na swój lokalny komputer używając poniższej komendy:
```
git clone https://github.com/zml18x/projektZaliczenie
```

### Krok 2: Przejście do katalogu projektu
Przejdź do katalogu projektu wpisując:
```
cd ProjektZaliczenie
```

### Krok 3: Uruchomienie kontenerów
Uruchom wszystkie kontenery używając Docker Compose:
```
docker-compose up
```

### Krok 4: Sprawdzenie kontenera backendu
Po uruchomieniu kontenerów sprawdź, czy kontener z backendem został prawidłowo uruchomiony. Jeśli nie, uruchom go ręcznie:
```
docker-compose up <nazwa_kontenera_backendu>
```

### Krok 5: Dostęp do aplikacji
Aplikacja powinna być teraz dostępna pod adresem:
```
localhost:4200
```
