import os
import json
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from app.core.enums import FuelType, DTCCodeSeverity


load_dotenv()


class DTCAnalysisResponse(BaseModel):
    severity: DTCCodeSeverity
    manager_explanation: str
    action_required: str


class DTCTranslator:
    def __init__(self, api_key: str = None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def analyze_error(self, dtc_code: str, raw_desc: str,
                      fuel_type: FuelType, car_profile: str,
                      car_brand: str) -> DTCAnalysisResponse:

        # ---------------------------------------------------------------------
        # WARSTWA 1: REGUŁY SZTYWNE (HARDCODED SAFETY RULES)
        # Chronią przed halucynacjami AI w kwestii krytycznego bezpieczeństwa
        # ---------------------------------------------------------------------
        desc_lower = raw_desc.lower()
        code_upper = dtc_code.upper()

        prefix = code_upper[0]
        numeric_part = code_upper[1:]

        # 1. Wypadanie zapłonów (Misfires): przedział od P0300 do P0312
        if prefix == 'P' and "0300" <= numeric_part <= "0312":
            return DTCAnalysisResponse(severity=DTCCodeSeverity.CRITICAL,
                                       manager_explanation="Wypadanie zapłonów. Kontynuacja jazdy grozi stopieniem katalizatora lub pożarem.",
                                       action_required="Zalecane natychmiastowe unieruchomienie pojazdu.")

        # Krytyczne bezpieczeństwo: Układ hamulcowy (błędy 'C' lub słowa kluczowe)
        if prefix == 'C' and "0000" <= numeric_part <= "008A":
            return DTCAnalysisResponse(severity=DTCCodeSeverity.CRITICAL,
                                       manager_explanation="Krytyczny błąd układu hamulcowego lub pompy ABS.",
                                       action_required="Wymagane natychmiastowe zatrzymanie pojazdu.")

        # Krytyczne bezpieczeństwo: Ciśnienie oleju (Zatarcie silnika)
        if "oil pressure" in desc_lower or ("ciśnien" in desc_lower and "olej" in desc_lower):
            return DTCAnalysisResponse(severity=DTCCodeSeverity.CRITICAL,
                                       manager_explanation="Krytyczne ryzyko natychmiastowego zatarcia silnika z powodu braku smarowania.",
                                       action_required="Wymagane natychmiastowe wyłączenie silnika.")

        # ---------------------------------------------------------------------
        # WARSTWA 2: ANALIZA AI (Dla błędów eksploatacyjnych, czujników, filtrów itp.)
        # ---------------------------------------------------------------------
        system_prompt = """Jesteś ekspertem telematycznym i analitykiem ryzyka w wypożyczalni samochodów.
            Twoim jedynym zadaniem jest ocena kodu błędu OBD-II pod kątem ryzyka biznesowego i technicznego DLA SPECYFICZNEGO TYPU POJAZDU.

            Zwróć odpowiedź WYŁĄCZNIE w formacie JSON o strukturze:
            {
                "severity": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
                "manager_explanation": "string",
                "action_required": "string"
            }

            <definicje_severity>
            - LOW: Brak ryzyka. Auto może bez problemu dokończyć wielodniowy wynajem.
            - MEDIUM: Drobna usterka podnosząca koszty (np. spalanie). Auto może dokończyć krótki wynajem.
            - HIGH: Ryzyko wejścia w tryb awaryjny (limp mode), unieruchomienia na trasie lub zapchania podzespołów (np. DPF). Zalecana szybka podmiana auta.
            - CRITICAL: Ekstremalne ryzyko zniszczenia silnika przy dalszej eksploatacji lub zagrożenie bezpieczeństwa. Wysokie koszty naprawy. Natychmiastowe zatrzymanie pojazdu. Absolutny zakaz dalszej jazdy na kołach, konieczność wezwania lawety
            </definicje_severity>

            <restrykcje_tekstowe>
            1. manager_explanation: MAKSYMALNIE 1 krótkie zdanie opisujące bezpośredni skutek dla danej klasy auta.
            2. action_required: MAKSYMALNIE 5-7 słów. Zakaz używania trybu rozkazującego. Używaj wyłącznie form: "Sugerowana...", "Zalecane...", "Możliwa konieczność...". Wynik w action_required must logicznie odpowiadać poziomowi severity.
            </restrykcje_tekstowe>

            <wazne_uwagi>
            - Usterki mechaniczne grożące zniszczeniem silnika (np. rozrząd, smarowanie) oraz usterki skrzyni biegów są niezależne od profilu pojazdu i ZAWSZE muszą otrzymywać priorytet CRITICAL, nawet dla aut miejskich.
            - Auta sportowe mają zakaz jazdy torowej
            </wazne_uwagi>

            <przyklady_wzorcowego_rozumowania>
            Przykład 1:
            Profil: Samochód dostawczy
            Kod: P0104 (Przepływomierz - sygnał przerywany)
            Wynik: {
                "severity": "HIGH",
                "manager_explanation": "Ryzyko nagłego wejścia silnika w tryb awaryjny i zablokowania procedury wypalania filtra DPF.",
                "action_required": "Sugerowana szybka podmiana pojazdu klientowi."
            }

            Przykład 2:
            Profil: Samochód miejski
            Kod: P0104 (Przepływomierz - sygnał przerywany)
            Wynik: {
                "severity": "MEDIUM",
                "manager_explanation": "Możliwe delikatne falowanie obrotów oraz nieznacznie podwyższone zużycie paliwa.",
                "action_required": "Zalecana weryfikacja przy najbliższym serwisie."
            }
            </przyklady_wzorcowego_rozumowania>"""

        user_prompt = f"""
        Kod błędu: {dtc_code}
        Opis techniczny: {raw_desc}

        PROFIL POJAZDU W WYPOŻYCZALNI: {car_profile}
        Rodzaj paliwa: {fuel_type.value}
        Marka pojazdu: {car_brand}

        Oceń ryzyko, biorąc pod uwagę jak ten specyficzny błąd wpływa na eksploatację TEGO KONKRETNEGO typu auta przez przypadkowego klienta wypożyczalni.
        """

        print('Odpowiedz AI')
        try:
            response = self.client.chat.completions.parse(
                model="gpt-5.6-luna",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format=DTCAnalysisResponse,
                # temperature=0.1
                reasoning_effort='high'
            )

            return response.choices[0].message.parsed

        except Exception as e:
            print(f"[ERROR] Błąd komunikacji z OpenAI: {e}")
            return {
                "severity": "UNKNOWN",
                "manager_explanation": "Błąd tłumaczenia diagnostyki AI.",
                "action_required": "Skontaktuj się z mechanikiem."
            }


if __name__ == '__main__':
    translator = DTCTranslator()

    # Lista testowa symulująca zmianę konfiguracji auta przez użytkownika w aplikacji Traflee
    test_cases = [
        'Średni sedan',
        # 'Samochód dostawczy',
        # 'Samochód sportowy'
    ]

    dtc_code = "P0455"
    desc = ""

    for car_type in test_cases:
        print(f"\n--- TEST DLA PROFILE: {car_type} ---")
        response = translator.analyze_error(dtc_code, desc, FuelType.PETROL, car_type, 'Audi')
        print(f'severity: {response.severity.value}\nmanager_explanation: {response.manager_explanation}\naction_required: {response.action_required}')
