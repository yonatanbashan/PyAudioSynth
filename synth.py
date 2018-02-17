import tkinter as tk
import program1


print ("Mysynth!")

def play_sound():
    program1.main_program()



def exit_program():
    #stream.stop_stream()
    #stream.close()
    #p.terminate()
    quit()

root = tk.Tk()
frame = tk.Frame(root)
frame.pack()

playButton = tk.Button(frame,
                   text="Play",
                   command=play_sound)
playButton.pack(side=tk.LEFT)
quitButton = tk.Button(frame,
                   text="Quit",
                   command=exit_program)
quitButton.pack(side=tk.LEFT)


root.mainloop()



