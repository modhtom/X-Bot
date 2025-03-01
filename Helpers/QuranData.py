import requests
import Email as email


def get_total_verses(surah_number):
    base_url = "http://api.alquran.cloud/v1/surah"
    endpoint = f"{base_url}/{surah_number}"
    response = requests.get(endpoint)
    numberOfAyahs = response.json()["data"]["numberOfAyahs"]
    end_verse = int(numberOfAyahs)
    return end_verse


def get_surah_text(surah_number, verse_number, edition):
    base_url = "http://api.alquran.cloud/v1/ayah"
    endpoint = f"{base_url}/{surah_number}:{verse_number}/{edition}"
    response = requests.get(endpoint)

    if response.status_code == 200:
        text = response.json()["data"]["text"]
        return f"{text}\n"
    else:
        return f"Error getting text for verse {verse_number}\n"


def get_surah_text_range(surah_number, start_verse, end_verse, edition):
    text_combined = ""
    for verse_num in range(int(start_verse), int(end_verse) + 1):
        verse_text = get_surah_text(surah_number, verse_num, edition)
        if verse_text:
            text_combined += verse_text
        else:
            email.send(f"Error getting text for verse {verse_num}")

    return text_combined


def QuranText(surah_number, start_verse, end_verse, edition="quran-simple"):
    text_combined = get_surah_text_range(surah_number, start_verse, end_verse, edition)

    if text_combined:
        output_file = f"Quran_Videos/Data/text/Surah_{surah_number}_Text_from_{start_verse}_to_{end_verse}.txt"
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(text_combined)
        # email.send(f"Combined text saved as '{output_file}'")
        return output_file
    else:
        email.send("Failed to get text.")
        return None


# Base URL for Quran API
API_BASE_URL = "https://api.alquran.cloud/v1"


def fetch_surah_with_translation(surah_number):
    try:
        response = requests.get(
            f"{API_BASE_URL}/surah/{surah_number}/editions/quran-uthmani,ar.muyassar"
        )
        if response.status_code == 200:
            return response.json().get("data", [])
        else:
            email.send(f"Error fetching data: {response.status_code}")
            return None
    except Exception as e:
        email.send(f"Error: {e}")
        return None
