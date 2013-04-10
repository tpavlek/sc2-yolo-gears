from Tkinter import *
from tkFileDialog import *
import calendar

class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.menuBar = Menu(master)
        
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
            self.c.create_oval(80+dx/2+i*dx, 370-data[i]*33/interval, 80+dx/2+i*dx, 370-data[i]*33/interval, fill = "black", width = 4)
            x.append(80+dx/2+i*dx)
            y.append(370-data[i]*33/interval)

        for i in range(len(data)-1):
            self.c.create_line(x[i],y[i],x[i+1],y[i+1])
        """

        b = Button(master, text = "APM", command = self.analyzeData)
        b.pack()

        #Table Display
        self.c.create_rectangle(25, 450, 1375, 875, outline="green", fill="black")
        for i in range(10):
            self.c.create_line(50, 450+42+42*i, 1325, 450+42+42*i, fill="green")
            self.c.create_text(40, 450+42/2+42*i, text = "P", fill="green")


    def selRep(self):
        filename = askopenfilename()
        #pass to troy's stuff
        print(filename)

    def selFol(self):
        dire = askdirectory()
        #pass to troy's stuff
        print(dire)
    
    def getDataAPM(self):
        file = open("processed.py", "r")
        repInfo = []

        for line in file:
            line = line.rstrip()
            fields = line.split(",")
            self.repInfo.append((fields[0], fields[1]))

        return repInfo

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
                data.append(avg/count)
                yr += 1
                count = 0
                avg = 0

        elif kwargs.get("time") == "month":
            mon = 1
            yr = kwargs.get("year")
            while not mon == 12:
                s = str(mon)
                if mon < 10:
                    s = str(0)+str(mon)
                for k in dic.keys():
                    if k.find(s, beg=5, end=8) != -1 and k.find(yr) != -1:
                        avg += int(dic.get(k))
                        count += 1
                data.append(avg/count)
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
                data.append(avg/count)
                day += 1
                count = 0
                avg = 0

        self.displayGraph(data, time)

    def displayGraph(self, data, time):
        if time == "year":
            #x axis
            dx = 320 
            yr = 2010
            for i in range(len(data)):
                self.c.create_line(80+dx+i*dx, 370, 80+dx+i*dx, 380)
                self.c.create_text(80+dx/2+i*dx, 380, text = str(yr))
                yr += 1
                    
        elif time == "month":
            #x axis
            dx = 103
            mon = 1
            for i in range(len(data)):
                self.c.create_line(80+dx+i*dx, 370, 80+dx+i*dx, 380)
                self.c.create_text(80+dx/2+i*dx, 380, text = calendar.month_name[mon])
                mon += 1         

        elif time == "day":
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
            self.c.create_oval(80+dx/2+i*dx, 370-data[i]*33/interval, 80+dx/2+i*dx, 370-data[i]*33/interval, fill = "black", width = 4)
            x.append(80+dx/2+i*dx)
            y.append(370-data[i]*33/interval)

        for i in range(len(data)-1):
            self.c.create_line(x[i],y[i],x[i+1],y[i+1])

    def displayTable(self, dic, **kwargs):
        if kwargs.get("type") == "winrate":
            for i in range(9):
                self.c.create_line(450+47+47*i, 50, 450+47+47*i, 1325)
                self.c.create_text(450+47/2+47*i, 40, text = "P")
           
def start():
    root = Tk()
    app = App(root)
    root.title("Sc2 Thing")
    root.mainloop()

if __name__ == "__main__":
    start()
    
