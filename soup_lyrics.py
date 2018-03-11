from bs4 import BeautifulSoup
import urllib.request
import html.parser
from collections import defaultdict

filter = {"the", "oh"}

def get_html(url: str) -> str:
    response = urllib.request.urlopen(url)
    data = response.read().decode("utf-8")
    return data

def get_lyrics(html_doc: str) -> str:
    soup = BeautifulSoup(html_doc, "html.parser")
    song_title = soup.find_all("b")[1]
    lyrics = song_title.find_next_sibling("div")
    return lyrics.get_text().strip()
    
def add_to_dictionary(lyrics_dict: {str: int}, lyrics: str) -> None:
    words = lyrics.split()
    for word in words:
        adding = alpha_lower(word)
        if adding not in filter:
            lyrics_dict[adding] += 1
    
def dict_to_str(lyrics_dict: {str: int}) -> str:
    result = ""
    sorted_dict = sorted(lyrics_dict.items(), key=lambda x: x[1], reverse=True)
    for (key, value) in sorted_dict:
        result += ("{}: {}\n".format(key, value))
    return result

def add_url_to_lyrics_dict(url: str, lyrics_dict: {str, int}) -> None:
    html_doc = get_html(url)
    lyrics = get_lyrics(html_doc)
    add_to_dictionary(lyrics_dict, lyrics)

def alpha_lower(s: str) -> str:
    return ''.join([c for c in s.lower() if c.isalpha()])

def write_to_file(file_name: str, data: str) -> None:
    with open(file_name, 'w') as file:
        file.write(data)

def get_az_url(song_info: str) -> str:
    base = "https://www.azlyrics.com/lyrics"
    info_list = song_info.split(":")
    artist, song = alpha_lower(info_list[0]), alpha_lower(info_list[1])
    return "{}/{}/{}.html".format(base, artist, song)

def main():
    lyrics_dict = defaultdict(int)
    input_file = open("songs.txt")
    for line in input_file:
        song_info = line.strip()
        try:
            add_url_to_lyrics_dict(get_az_url(song_info), lyrics_dict)
        except(urllib.error.HTTPError):
            print("URL not available: {}".format(song_info))
    input_file.close()
    write_to_file("frequency.txt", dict_to_str(lyrics_dict))


if __name__ == "__main__":
    main()