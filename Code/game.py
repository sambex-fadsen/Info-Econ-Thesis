import tkinter

window = tkinter.Tk()
window.title("Prediction Market Simulator")
label = tkinter.Label(window, text = "Submit your report!")
label.pack()
button = tkinter.Button(window,text="Report")
button.pack()
window.mainloop()
