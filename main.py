from application import *

root=tk.Tk()
root.protocol('WM_DELETE_WINDOW', lambda: close_application(root))
root.resizable(height=False, width=False)
#root.overrideredirect(True) # remove title bar
window_x = (root.winfo_screenwidth() / 2) - (root.winfo_fpixels('8i') / 1.5)
window_y = (root.winfo_screenheight() / 2) - (root.winfo_fpixels('6i') / 1.5)
root.geometry('+%d+%d' % (window_x, window_y))  

app=Application(master=root)
app.mainloop()