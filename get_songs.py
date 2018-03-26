from bs4 import BeautifulSoup
from soup_lyrics import get_html

base_url = "http://billboardtop100of.com/"

def get_url(year: int) -> str:
    return "{}{}-2/".format(base_url, year)

def add_songs_from_year(song_list: [(str, str)], year: int, song_amount: int) -> [(str, str)]:
    html_doc = get_html(get_url(year))
    soup = BeautifulSoup(html_doc, "html.parser")
    songs = soup.tbody.find_all("tr")
    for child in songs:
        if int(child.contents[1].string) <= song_amount:
            song_list.append("{}: {}".format(child.contents[3].string, child.contents[5].string))
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
        file.write(item)
        file.write("\n")
    file.close()


def main():
    print("Fetching songs...")
    song_list = add_songs_in_range([], 1963, 2012, 20)
    print("Writing to file...")
    write_list_to_file("songs.txt", song_list)
    print("Done")

if __name__=="__main__":
    main()