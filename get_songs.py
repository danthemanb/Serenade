from bs4 import BeautifulSoup
from soup_lyrics import get_html

base_url = "https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of"

def get_url(year: int) -> str:
    return "{}_{}".format(base_url, year)

def get_info(song_info: BeautifulSoup) -> (int, str, str):
    info = song_info.contents
    number = int(info[1].string) if info[1].string != "Tie" else 0
    title_info = info[3].contents
    title = title_info[1].string if len(title_info) > 1 else title_info[0].strip('"')
    artist = info[5].string if info[5].string else info[5].contents[0].string
    return (number, title, artist)

def add_songs_from_year(song_list: [(str, str)], year: int, song_amount: int) -> [(str, str)]:
    html_doc = get_html(get_url(year))
    soup = BeautifulSoup(html_doc, "html.parser")
    songs = soup.table.find_all("tr")[1:]
    for child in songs:
        number, title, artist = get_info(child)
        if number <= song_amount:
            song_list.append((title, artist))
        else:
            break
    return song_list

def add_songs_in_range(song_list: [(str, str)], start: int, end: int, song_amount: int) -> [(str, str)]:
    for i in range(start, end+1):
        song_list = add_songs_from_year(song_list, i, song_amount)
    return song_list

def write_list_to_file(file_name: str, to_write: list):
    file = open(file_name, "w")
    for item in to_write:
        try:
            file.write("{}: {}\n".format(item[0], item[1]))
        except UnicodeEncodeError:
            print("Can't write character")
    file.close()


def main():
    print("Fetching songs...")
    song_list = add_songs_in_range([], 1963, 2017, 100)
    print("Writing to file...")
    write_list_to_file("songs.txt", song_list)
    print("Done")

if __name__=="__main__":
    main()