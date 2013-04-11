from Tkinter import *
from tkFileDialog import *
import calendar
import processed_replays

class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.menuBar = Menu(master)
        self.username = 'bonywonix' #this is a default for demo - in future versions this would be set via a config file 
        self.replayPath = "replays/" #default
        self.replays = None # This is so we can check for instances later
        
        #Replay Menu

        self.Rep = Menu(self.menuBar, tearoff = 0)
        self.menuBar.add_cascade(label='Replays', menu=self.Rep)       
              
        self.Rep.add_command(label = 'Select Replay', command=self.selRep)
        self.Rep.add_command(label = 'Select Folder', command=self.selFol)

        #Edit Menu

        self.Ed = Menu(self.menuBar, tearoff = 0)
        self.menuBar.add_cascade(label='Edit', menu=self.Ed)  
          
        self.Ed.add_command(label = 'Preferences', command=self.showPrefs)

        #Help Menu

        self.Help = Menu(self.menuBar, tearoff = 0)
        self.menuBar.add_cascade(label='Help', menu=self.Help)
        self.Help.add_command(label = 'About', command = self.showHelp)

        master.config(menu = self.menuBar)

        #canvas to draw graph on
        
        self.c = Canvas(master, width=1400, height=900)
        self.c.pack()
        
        #Graph Display
        self.c.create_rectangle(25,25,1375,400, outline="blue", fill="white")
        self.c.create_line(80, 370, 1320, 370, arrow=LAST)  #horizontal
        self.c.create_line(80, 30, 80, 370, arrow=FIRST)    #vertical
 
        self.analyzeData(self.getAPMDict(), time ="month", year = "2013")
        
        #A button for future implementations where graph shows things other than APM
        #b = Button(frame, text = "APM", command = self.analyzeData(self.getAPMDict(), time ="month", year = "2013" ))
        #b.pack()

        #Table Display
        self.c.create_rectangle(25, 450, 1375, 875, outline="green", fill="black")
        self.displayTable(self.getWRDict(), type="winrate")

        # We're done with init

    def showHelp(self):
        """
        The help window including author information
        """
        popup = Toplevel()
        popup.title("About SC2-YOLO-Gears")
        about_message = "By Andy Yao and Troy Pavlek. You should use SC2Gears instead"
        msg = Message(popup, text=about_message)
        msg.pack()

        button = Button(popup, text="Close", command=popup.destroy)
        button.pack()

    def showPrefs(self):
        """
        Preferences Dialog
        """
        popup = Toplevel()
        popup.title("Edit Preferences")

        msg = Message(popup, text="Choose username:");
        msg.pack()

        editField = Entry(popup)
        editField.delete(0, END)
        editField.insert(0, self.username)
        editField.pack()

        submit = Button(popup, text="Submit", command = lambda e = editField.get(), x = popup: self.editPrefs(e, x))
        submit.pack()

    def editPrefs(self, newUser, popup):
        """
        Edits the preferences in the object state
        In future implementations would write to a configuration file
        Takes a string with a new username preference and the object reference of the edit dialog to destroy
        """
        self.username = newUser
        popup.destroy()


    def selRep(self):
        """
        Doesn't serve a useful function curently, but might in future implementations
        (Individual replay analysis, would require restructuring of the UX to accomadate for the graph
        disappearing)
        """
        filename = askopenfilename()
        #self.replayPath = filename

    def selFol(self):
        """
        Prompts the user for a new folder and sets the internal object state to that folder
        """
        dire = askdirectory()
        self.replayPath = dire
        
        # These should be refactored out into a redraw function in the future
        self.clearGraph()
        self.clearTable()
        self.analyzeData(self.getAPMDict(True), time = "month", year="2013")
        self.displayTable(self.getWRDict(), type="winrate") # no need for reload since we just did

    def getAPMDict(self, reload = False):
        """
        If this is the first time we're asking for APM or WR then we need to process all the replays 
        (may take a while). We can also force the reprocessing witht he optional reload argument
        """
        if self.replays is None or reload:
            self.replays = processed_replays.ProcessedReplays(self.username, self.replayPath)
        return self.replays.getAPM()

    def getWRDict(self, reload = False):
        if self.replays is None or reload:
            self.replays = processed_replays.ProcessedReplays(self.username, self.replayPath)
        return self.replays.getWinrates()

    def selGraph(self, *args, **kwargs):
        """
        Selects the graph to display, and then hands it off to analyzeData for processing.
        kwargs contains:
        TODO ANDY FILL THIS
        """
        if kwargs.get("time") == "year":
            self.clearGraph()
            self.analyzeData(self.getAPMDict(), time = "year")
	
        elif kwargs.get("time") == "month":
            self.clearGraph()
            self.analyzeData(self.getAPMDict(), time = "month", year = kwargs.get("year"))

        elif kwargs.get("time") == "day":
            self.clearGraph()
            self.analyzeData(self.getAPMDict(), time = "day", year = kwargs.get("year"), month = kwargs.get("month"))

    def analyzeData(self, dic, **kwargs):
        """
        Takes a dictionary of average APMs along with potenital arguments.
        kwargs contains:
        TODO ANDY FILL THIS
        """

        avg = 0
        count = 0
        data = []
        
        if kwargs.get("time") == "year":
            yr = 2010
            mon = 0
            while not yr == 2014:
                for k in dic.keys():
                    if k.find(str(yr)) != -1:
                        avg += int(dic.get(k))
                        count += 1
                if count:
                    data.append(avg/count)
                else:
                    data.append(0)
                yr += 1
                count = 0
                avg = 0

        elif kwargs.get("time") == "month":
            mon = 1
            yr = kwargs.get("year")
            while not mon == 13:
                s = str(mon)
                if mon < 10:
                    s = str(0)+str(mon)
                for k in dic.keys():
                    if k.find(s, 4, 7) != -1 and k.find(yr) != -1:
                        avg += int(dic.get(k))
                        count += 1
                if count:
                    data.append(avg/count)
                else:
                    data.append(0)

                mon += 1
                count = 0
                avg = 0
        
        elif kwargs.get("time") == "day":
            day = 1
            yr = kwargs.get("year")
            mon = kwargs.get("month")
            while not day == 32:
                s = str(day)
                if day < 10:
                    s = str(0)+str(day)
                m = str(list(calendar.month_name).index(mon))
                if m < 10:
                    m = str(0)+str(m)
                for k in dic.keys():
                    if k.find(s, 7, 10) != -1 and k.find(yr) != -1 and k.find(m, 4, 7) != -1:
                        avg += int(dic.get(k))
                        count += 1
                if count:
                    data.append(avg/count)
                else:
                    data.append(0)

                day += 1
                count = 0
                avg = 0

        #print(data)
        self.displayGraph(data, kwargs.get("time"), year = yr, month = mon)

    def displayGraph(self, data, time, **kwargs):
        if time == "year":
            #x axis
            dx = 320 
            yr = 2010
            self.c.create_text(700, 40, text = "Yearly Progress")
            for i in range(4):
                self.c.create_line(80+dx+i*dx, 370, 80+dx+i*dx, 380)
                self.c.create_text(80+dx/2+i*dx, 380, text = str(yr), tags=str(yr), activefill="Red")
                #self.c.tag_bind(str(yr),"<ButtonPress-1>", lambda e, y = yr: self.selGraph(time="month", year=str(y)))
                yr += 1
            for e in self.c.find_all():
                print self.c.gettags(e)
        

        elif time == "month":
            #x axis
            dx = 103
            mon = 1
            Yid = self.c.create_text(700, 40, text = "Monthly Progress " + kwargs.get("year"), tags=kwargs.get("year"), activefill = "Red")
            self.c.tag_bind(Yid, "<ButtonPress-1>", lambda e: self.selGraph(time = "year"))
            for i in range(12):
                self.c.create_line(80+dx+i*dx, 370, 80+dx+i*dx, 380)
                self.c.create_text(80+dx/2+i*dx, 380, text = calendar.month_name[mon], tags=calendar.month_name[mon], activefill = "Red")
                self.c.tag_bind(calendar.month_name[mon],"<ButtonPress-1>", lambda e, m = mon: self.selGraph(time="day", year = kwargs.get("year"), month=calendar.month_name[m]))    
                mon += 1         
            
        elif time == "day":
            #x axis
            dx = 40
            day = 1
            self.c.create_text(700, 40, text = "Daily Progress " + kwargs.get("month") + kwargs.get("year"), tags=kwargs.get("month"), activefill = "Red")
            self.c.tag_bind(kwargs.get("month"), "<ButtonPress-1>", lambda e: self.selGraph(time="month", year = kwargs.get("year")))

            for i in range(31):
                self.c.create_line(80+dx+i*dx, 370, 80+dx+i*dx, 380)
                self.c.create_text(80+dx/2+i*dx, 380, text = str(day), tags=str(day))
                day += 1

        #y axis
        interval = float(max(data) - min(data))/10
        if not interval:
            interval = 10        

        for i in range(11):
            self.c.create_line(70, 370-i*33, 80, 370-i*33)
            self.c.create_text(60, 370-i*33, text = str(min(data)+i*interval))

        #generate points and lines
        x = []
        y = []
        for i in range(len(data)):
            self.c.create_oval(80+dx/2+i*dx, 370-data[i]*33/interval, 80+dx/2+i*dx, 370-data[i]*33/interval, fill = "blue", width = 4)
            x.append(80+dx/2+i*dx)
            y.append(370-data[i]*33/interval)

        for i in range(len(data)-1):
            self.c.create_line(x[i],y[i],x[i+1],y[i+1], fill="blue")

    def clearGraph(self, *args):
        self.c.create_rectangle(25,25,1375,400, outline="blue", fill="white")
        self.c.create_line(80, 370, 1320, 370, arrow=LAST)  #horizontal
        self.c.create_line(80, 30, 80, 370, arrow=FIRST)    #vertical


    def displayTable(self, dic, **kwargs):
        if kwargs.get("type") == "winrate":
            race = ["Protoss", "Terran", "Zerg"]
            MU = ["PvP", "PvT", "PvZ", "TvP", "TvT", "TvZ", "ZvP", "ZvT", "ZvZ"]
            self.c.create_text(295, 471, text = "Wins", fill="green")
            self.c.create_text(295+411, 471, text = "Losses", fill="green")
            self.c.create_text(295+411*2, 471, text = "Win Rate", fill="green")

	    # horizontal
            for i in range(10):
                self.c.create_line(50, 450+42+42*i, 1324, 450+42+42*i, fill="green")
                if i > 0:
                    self.c.create_text(70, 450+42/2+42*i, text = MU[i-1], fill="green")
	    #vertical
            for i in range(4):
                self.c.create_line(90+i*411, 462, 90+i*411, 870, fill="green")

            for i in range(3):
                d2 = dic.get(race[i])
                for r2 in d2.keys():
                    if r2 == "Protoss":
                        if d2[r2][1] != 0:
                            self.c.create_text(295, 513+i*126, text=d2[r2][0], fill="green")
                            self.c.create_text(295+411, 513+i*126, text=d2[r2][1]-d2[r2][0], fill="green")
                            self.c.create_text(295+411*2, 513+i*126, text=float(d2[r2][0])/d2[r2][1] *100, fill="green")

                    elif r2 == "Terran":
                        if d2[r2][1] != 0:
                            self.c.create_text(295, 513+42+i*126, text=d2[r2][0], fill="green")
                            self.c.create_text(295+411, 513+42+i*126, text=d2[r2][1]-d2[r2][0], fill="green")
                            self.c.create_text(295+411*2, 513+42+i*126, text=float(d2[r2][0])/d2[r2][1] *100, fill="green")

                    elif r2 == "Zerg":
                        if d2[r2][1] != 0:
                            self.c.create_text(295, 513+84+i*126, text=d2[r2][0], fill="green")
                            self.c.create_text(295+411, 513+84+i*126, text=d2[r2][1]-d2[r2][0], fill="green")
                            self.c.create_text(295+411*2, 513+84+i*126, text=float(d2[r2][0])/d2[r2][1] *100, fill="green")

    def clearTable(self):
        self.c.create_rectangle(25, 450, 1375, 875, outline="green", fill="black")
           
def start():
    root = Tk()
    app = App(root)
    root.title("Sc2 Thing")
    root.mainloop()

if __name__ == "__main__":
    start()
    
