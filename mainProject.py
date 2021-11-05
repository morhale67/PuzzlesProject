import PuzzleClass as Puzzle
import PySimpleGUI as sg
from Demo import demo

#  input window

# style:
sg.theme('DarkAmber')
window_title = 'Create your own puzzle!'
font = ("Arial", 13)
# content:
select_width = [sg.Text('Select one->'), sg.Listbox(['2', '3', '4', '5', '6', '7', '8', '9', '10'],
                                                    size=(2, 8), key='width', default_values='2')]
select_length = [sg.Text('Select one->'), sg.Listbox(['2', '3', '4', '5', '6', '7', '8', '9', '10'],
                                                     size=(2, 8), key='length', default_values='2')]

default_path = r'C:\Users\user\Desktop\PuzzleProject\Pictures\BabyMoana.jpg'
brows_line = [sg.T('Enter Image Path (JPG)'), sg.In(default_path, key='image_path', size=(55, 10)),
              sg.FileBrowse(), sg.Stretch()]
ok_cancel_bottom = [sg.Button('Ok'), sg.Button('Cancel')]

# create window:
window = sg.Window(window_title)
event = 'not_done'
event, values = sg.Window(window_title, [select_width, select_length, brows_line, ok_cancel_bottom], font=font).read(
    close=True)

if event == 'Ok':
    image_path = values['image_path']
    width, length = int(values['width'][0]), int(values['length'][0])
    try:
        new_puzzle = Puzzle.PuzzlePicture(image_path, width, length)
        solved_puzzle = new_puzzle.solve_puzzle()
        print("ALL DONE")
    except:
        sg.popup_cancel('something went wrong, please check your input:', image_path, width, length)
else:
    sg.popup_cancel('User aborted')
