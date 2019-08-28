# Future updates:
# 1. Improve design
# 2. Add Player with which user can listen to the song
# 3. To be continued...


import lyricsgenius

import sys
from PyQt5.QtWidgets import *

# token for the access to lyricsgenius API from https://genius.com
genius = lyricsgenius.Genius('01-s0pOLPdFfSQQSw3UQtLU-x6Oc8L8bshd8jOYV-mw0_rAym18M-FUGEKrir2uI')


class App(QWidget):

    def __init__(self):
        super(App, self).__init__()

        # Initial conditions for the Desktop App
        self.setFixedWidth(500)
        self.setFixedHeight(480)

        self.list = []
        self.scroll = QScrollBar()
        self.scroll_value = 0
        self.artist_input = QLineEdit()
        self.song_input = QLineEdit()
        self.artist = QLabel('Artist Name:')
        self.song = QLabel('Song Name:')
        self.lyrics = QLabel('')
        self.gui()

    def gui(self):
        self.setWindowTitle('Find Lyrics')
        self.setGeometry(300, 300, 500, 480)

        # grid to display labels and their inputs
        grid = QGridLayout()
        grid.setSpacing(10)

        # Labels and Inputs for artist and song name
        self.artist_input.setFixedWidth(300)
        self.song_input.setFixedWidth(300)
        self.artist.setFixedWidth(100)
        self.song.setFixedWidth(100)

        # place them inside grid
        grid.addWidget(self.artist, 1, 0)
        grid.addWidget(self.artist_input, 1, 1)

        grid.addWidget(self.song, 2, 0)
        grid.addWidget(self.song_input, 2, 1)

        grid.addWidget(self.lyrics, 4, 0, 1, 3)

        self.setLayout(grid)

        # button to find lyrics for given artist and song name
        find = QPushButton('Find Lyrics', self)
        find.resize(find.sizeHint())
        find.clicked.connect(self.onclick)

        # button to clear lyrics and inputs
        clear = QPushButton('Clear', self)
        clear.resize(clear.sizeHint())
        clear.clicked.connect(self.clear)

        # add buttons to grid
        grid.addWidget(find, 3, 0)
        grid.addWidget(clear, 3, 2)

        # scroll with initial condition being invisible if # of lines < 20
        self.scroll.setMaximum(150)
        self.scroll.setVisible(False)
        self.scroll.sliderMoved.connect(self.slider)
        grid.addWidget(self.scroll, 4, 4)

        # Show Desktop App
        self.show()

    # If Find button is clicked, start searching lyrics
    def onclick(self):
        # get text from inputs
        artist = self.artist_input.text()
        song = self.song_input.text()
        print(artist, song)
        # if one of the inputs empty show text below
        if artist == '' or song == '':
            self.lyrics.setText('Please fill both inputs')

        # if input is not empty
        else:
            # run API to search lyrics
            result = genius.search_song(song, artist)
            lyrics = result.lyrics
            # convert lyrics in the form of string to list by splitting it
            self.list = str(lyrics).split('\n')
            # print(lyrics)
            s = ''
            # if # of lines > 20 show scroll and display first 20 lines of the lyrics
            if len(self.list) > 20:
                self.scroll.setVisible(True)
                self.scroll.setMaximum(len(self.list) - 20)
                i = 0
                for line in self.list:
                    s += line + '\n'
                    i += 1
                    if i == 20:
                        break
            else:
                for line in self.list:
                    s += line + '\n'

            # display lyrics
            self.lyrics.setText(s)

    # if Clear button is clicked, reset inputs, lyrics and hide scroll
    def clear(self):
        self.artist_input.setText('')
        self.song_input.setText('')
        self.lyrics.setText('')
        self.scroll.setVisible(False)

    # if scroll is moved
    def slider(self):
        s = ''
        # if scroll is moved either up or down
        if self.scroll.value() != self.scroll_value:
            if 0 < self.scroll.value() < 3:
                index = 0
            elif len(self.list) - 23 < self.scroll.value() < len(self.list) - 20:
                index = len(self.list) - 20
            else:
                index = self.scroll_value

            # by using variable index from above display text from the list defined
            # after getting lyrics from API
            for i in range(index, 20 + index):
                s += self.list[i] + '\n'

        else:
            return

        # display lyrics and update scroll value for future moves
        self.lyrics.setText(s)
        self.scroll_value = self.scroll.value()


# main method that runs Desktop app
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())