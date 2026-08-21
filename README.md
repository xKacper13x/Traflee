# Traflee
Zbudować to na maszynie EC2 w AWS


Potrzebne komponenty do auta:

-Profesjonalny moduł OBD z GSM
    Co ma w środku: Wbudowany modem komórkowy (GSM), moduł GPS (do śledzenia tras i sprawdzania, gdzie wystąpił błąd silnika) i własną pamięć wewnętrzną (która gromadzi dane, jeśli auto np. wjedzie do podziemnego garażu i straci zasięg, by wysłać je później). Nie trzeba kleić żadnych zewnętrznych anten na szybach – wszystko jest zamknięte w jednej obudowie.

-Karta SIM M2M (Łączność)

-Rozgałęziacz OBD / Kabel Y (Branżowy "sekret")

To opcjonalny, ale absolutnie kluczowy element przy pracy z wypożyczalniami i kurierami, o którym rzadko mówi się głośno. Rozwiązuje dwa potężne problemy:

    Problem z odłączaniem: Jeśli kostka wystaje bezpośrednio z gniazda pod kolanami kierowcy, pracownik lub klient może ją złośliwie (żeby go nie śledzono) lub przypadkowo wykopnąć butem.

    Problem z mechanikami: Gdy auto trafia na serwis, mechanik potrzebuje wolnego portu OBD. Wyciągnie Twój sprzęt i na 90% zapomni wpiąć go z powrotem.

    Rozwiązanie: Dokupujesz płaski przedłużacz-rozgałęziacz (tzw. "kabel Y") za kilkadziesiąt złotych. Oryginalne gniazdo auta wypina się z plastiku, wpina się w nie rozgałęziacz, a samą kostkę GSM chowa głęboko pod deską rozdzielczą (np. przypinając opaską zaciskową). W widoczne, oryginalne miejsce wsuwa się nową, pustą końcówkę rozgałęziacza. Dzięki temu złodziej/kierowca w ogóle nie widzi urządzenia, mechanik ma wolny port diagnostyczny, a system bezpiecznie działa w ukryciu.