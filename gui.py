from Tkinter import *
from tkFileDialog import *
import calendar
import processed_replays

class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.menuBar = Menu(master)
        self.username = 'bonywonix' #TODO this needs to be set via preferences window
        self.replayPath = "replays/"
        self.replays = None # This is so we can check for instances later
        
        #Replay Menu

        self.Rep = Menu(self.menuBar, tearoff = 0)
        self.menuBar.add_cascade(label='Replays', menu=self.Rep)       
              
        self.Rep.add_command(label = 'Select Replay', command=self.selRep)
        self.Rep.add_command(label = 'Select Folder', command=self.selFol)

        #Edit Menu

        self.Ed = Menu(self.menuBar, tearoff = 0)
        self.menuBar.add_cascade(label='Edit', menu=self.Ed)  
          
        self.Ed.add_command(label = 'Preferences')

        #Help Menu

        self.Help = Menu(self.menuBar, tearoff = 0)
        self.menuBar.add_cascade(label='Help', menu=self.Help)
        self.Help.add_command(label = 'About')

        master.config(menu = self.menuBar)

        
        self.c = Canvas(master, width=1400, height=900)
        self.c.pack()
        
        #Graph Display
        self.c.create_rectangle(25,25,1375,400, outline="blue", fill="white")
        self.c.create_line(80, 370, 1320, 370, arrow=LAST)  #horizontal
        self.c.create_line(80, 30, 80, 370, arrow=FIRST)    #vertical
 
        """
        data = [0,50,25,30,44,54,2,345,56,111,45,76,200,86,220,50,25,30,44,54,2,345,56,111,45,76,200,86,22,98,67]
#x axis
        dx = 40
        day = 1
        for i in range(len(data)):
            self.c.create_line(80+dx+i*dx, 370, 80+dx+i*dx, 380)
            self.c.create_text(80+dx/2+i*dx, 380, text = str(day))
            day += 1

        #y axis
        interval = (max(data) - min(data))/10
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
            self.c.create_line(x[i],y[i],x[i+1],y[i+1],fill = "blue")
	"""
	self.analyzeData(self.getAPMDict(), time ="month", year = "2013")
        #b = Button(frame, text = "APM", command = self.analyzeData(self.getAPMDict(), time ="month", year = "2013" ))
        #b.pack()

        #Table Display
        self.c.create_rectangle(25, 450, 1375, 875, outline="green", fill="black")
	"""
	MU = ["PvZ", "PvT", "PvP", "ZvZ", "ZvT", "ZvP", "TvZ", "TvT", "TvP"]
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
	"""

    def selRep(self):
        filename = askopenfilename()
        self.replayPath = filename

    def selFol(self):
        dire = askdirectory()
        self.replayPath = dire
        print( self.getAPMDict())
        self.analyzeData(self.getAPMDict(), time = "year")

    def getAPMDict(self):
        if self.replays is None:
            self.replays = processed_replays.ProcessedReplays(self.username, self.replayPath)
        return self.replays.getAPM()

    def getWRDict(self):
        if self.replays is None:
            self.replays = processed_replays.ProcessedReplays(self.username, self.replayPath)
        return self.replays.getWinrate()

    def selGraph(self, *args, **kwargs):
	if kwargs.get("time") == "year":
	    self.clearGraph()
	    self.analyzeData(self.getAPMDict(), time = "year")
	
	elif kwargs.get("time") == "month":
            self.clearGraph()
            self.analyzeData(self.getAPMDict(), time = "month", year = kwargs.get("year"))

        elif kwargs.get("time") == "day":
            self.clearGraph()
            self.analyzeData(self.getAPMDict(), time = "day", year = kwargs.get("year"), month = kwargs.get("month"))

    def debug(self, *args):
        print("a")

    def analyzeData(self, dic, **kwargs):
        """
        Takes a dictionary of average APMs along with potenital arguments. The optional
        arguments are:
        """

        avg = 0
        count = 0
        data = []
        if kwargs.get("time") == "year":
            yr = 2010
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
                    if k.find(s, 5, 8) != -1 and k.find(yr) != -1:
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
            while not day == 31:
                s = str(day)
                if day < 10:
                    s = str(0)+str(mon)
                for k in dic.keys():
                    if k.find(s, beg=5, end=8) != -1 and k.find(yr) != -1 and k.find(mon) != -1:
                        avg += int(dic.get(k))
                        count += 1
                if count:
                    data.append(avg/count)
                else:
                    data.append(0)

                day += 1
                count = 0
                avg = 0

        self.displayGraph(data, kwargs.get("time"), year = yr, month = mon)

    def displayGraph(self, data, time, **kwargs):
        if time == "year":
            #x axis
            dx = 320 
            yr = 2010
            self.c.create_text(700, 40, text = "Yearly Progress")
            for i in range(len(data)):
                self.c.create_line(80+dx+i*dx, 370, 80+dx+i*dx, 380)
                self.c.create_text(80+dx/2+i*dx, 380, text = str(yr), tags=str(yr), activefill="Red")
                self.c.tag_bind(str(yr),"<ButtonPress-1>", lambda e: self.selGraph(time="month", year=str(yr)))
                yr += 1
                    
        elif time == "month":
            #x axis
            dx = 103
            mon = 1
            Yid = self.c.create_text(700, 40, text = "Monthly Progress " + kwargs.get("year"), tags=kwargs.get("year"), activefill = "Red")
            self.c.tag_bind(Yid, "<ButtonPress-1>", lambda e: self.selGraph(time = "year"))
            for i in range(len(data)):
                self.c.create_line(80+dx+i*dx, 370, 80+dx+i*dx, 380)
                self.c.create_text(80+dx/2+i*dx, 380, text = calendar.month_name[mon], tags=calendar.month_name[mon], activefill = "Red")
                self.c.tag_bind(calendar.month_name[mon],"<ButtonPress-1>", lambda e: self.selGraph(time="day", year = kwargs.get("year"), month=calendar.month_name[mon]))

                mon += 1         

        elif time == "day":
            #x axis
            dx = 40
            day = 1
            self.c.create_text(700, 40, text = "Daily Progress " + kwargs.get("month") + kwargs.get("year"), tags=kwargs.get("month"), activefill = "Red")
            self.c.tag_bind(kwargs.get("month"), "<ButtonPress-1>", lambda e: self.selGraph(time="year", year = kwargs.get("year")))

            for i in range(len(data)):
                self.c.create_line(80+dx+i*dx, 370, 80+dx+i*dx, 380)
                self.c.create_text(80+dx/2+i*dx, 380, text = str(day), tags=str(day))
                day += 1

        #y axis
        if len(data) > 1:
            interval = float(max(data) - min(data))/10
        
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
            MU = ["PvZ", "PvT", "PvP", "ZvZ", "ZvT", "ZvP", "TvZ", "TvT", "TvP"]
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

           
def start():
    root = Tk()
    app = App(root)
    root.title("Sc2 Thing")
    root.mainloop()

if __name__ == "__main__":
    start()
    
