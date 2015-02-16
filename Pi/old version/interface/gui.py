import Tkinter as tk
import picamera as pc
from detect import detect
import tkMessageBox

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.camera=pc.PiCamera()
        self.pack()
        self.createWidgets()
        self.createWidget2()
        self.createWidget3()
        self.createWidget4()
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)    
        master.overrideredirect(True)        
        master.config(bg='black')
        
    def callback_preview(self):
        self.camera.preview_fullscreen=False
        self.camera.preview_window=(50,50,320,200)
        self.camera.resolution=(320,200)
        self.camera.start_preview()

    def callback_stop(self):
        self.camera.stop_preview()

    def capture(self):
        self.camera.capture('test.jpg')
        userdata = detect()
        name=userdata[0]['name']
        energy=userdata[0]['energy']
        fat=userdata[0]['fat']
        saturates=userdata[0]['saturates']
        salt=userdata[0]['salt']
        sugars=userdata[0]['sugars']
        tkMessageBox.showinfo( 'name: ',name,'energy: ',energy,'fat: ',fat,'sugars: ',sugars,'salt: ',salt)
        text = Text(root)
        text.insert(INSERT, "name: ",name)
        text.insert(END, "Bye Bye.....")
        text.pack()

            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

    def createWidgets(self):
        self.hi_there = tk.Button(self)
        self.QUIT = tk.Button(self, text="QUIT", fg="red",
                                            command=root.destroy)
        self.pack()  
        self.pack(side = "top", fill="both", expand=True)
        # self.pack(expand = 0)
        self.QUIT.pack(side="left")
        # self["geometry"] = "200x100"
        
    def createWidget2(self):
        self.hi_there = tk.Button(self)
        self.QUIT = tk.Button(self, text="camera start", fg="red",
                                            command=self.callback_preview)
        self.pack()
        self.pack(side = "top", fill="both", expand=True)
        # self.pack(expand = 0)
        self.QUIT.pack(side="bottom")
        
    def createWidget3(self):
        self.hi_there = tk.Button(self)
        self.QUIT = tk.Button(self, text="camera stop", fg="red",
                                            command=self.callback_stop)
        self.pack()
        self.pack(side = "top", fill="both", expand=True)
        # self.pack(expand = 0)
        self.QUIT.pack(side="bottom")

    def createWidget4(self):
        self.hi_there = tk.Button(self)
        self.QUIT = tk.Button(self, text="capture", fg="red",
                                            command=self.capture)
        self.pack()
        self.pack(side = "top", fill="both", expand=True)
        # self.pack(expand = 0)
        self.QUIT.pack(side="right")


root = tk.Tk()
app = Application(master=root)
app.mainloop()


