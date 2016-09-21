#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from Tkinter import *
from os import *
import time
import tkMessageBox
import tkFileDialog

class simpleapp_tk(Tk):
    def __init__(self,parent):
        Tk.__init__(self,parent)
        self.parent = parent
        self.update_idletasks()
        width = 1280
        height = 600
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.initialize()

    def initialize(self):
        self.grid()

        label1 = Label(self, text='File Name', anchor='w', pady=5)
        label1.grid(row=0, sticky='W')

        self.entry_var1 = StringVar()
        self.entry1 = Entry(self, textvariable=self.entry_var1)
        self.entry1.grid(row=1,sticky=E+W+N+S, pady=5, columnspan=2)
        self.entry_var1.set(u"Enter the File Name")
        self.entry1.bind('<Return>',self.OnPressEnter)

        label2 = Label(self, text='Path to search', anchor='w')
        label2.grid(row=2, sticky='W', pady=5)

        self.entry_var2 = StringVar()
        self.entry2 = Entry(self, textvariable=self.entry_var2)
        self.entry2.grid(row=3,sticky=E+W+N+S, columnspan=2)
        self.entry_var2.set(u"Enter the File Path")
        self.entry2.bind("<Return>",self.OnPressEnter)
        
        dir_button = Button(self,text=u"Browse", command=self.askdirectory).grid(column=2,row=3, sticky='W')
        self.dir_opt = options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = False
        options['parent'] = self
        options['title'] = 'Choose a Folder'
        
        button = Button(self,text=u"Click to Search",command=self.OnButtonClick)
        button.grid(column=0,row=4,sticky='W',pady=7)

        label3 = Label(self, text=u'Results (Click on a file to open)', anchor='w')
        label3.grid(column=0, row=5, sticky='W')

        label5 = Label(self, text=u'Type an extension to filter', anchor='w')
        label5.grid(column=1, row=5, sticky='E')

        self.entry_var3 = StringVar()
        self.entry3 = Entry(self, textvariable=self.entry_var3)
        self.entry3.grid(row=5,sticky=E+W+N+S, column=2)
        self.entry_var3.set(u"Enter the file extension")
        self.entry3.bind("<Return>",self.Onextenter)

        self.label4_text = StringVar()
        label4 = Label(self, anchor='w',textvariable=self.label4_text, fg='white', bg='blue')
        label4.grid(column=0, row=6, columnspan=2, sticky='EW')
        self.label4_text.set(u"Time taken in secs: 0.0")

        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(7,weight=5)
        self.resizable(True,True)
        
        self.lb = Listbox(self, bg='light cyan')
        self.lb.grid(row=7,columnspan=3, rowspan=20, sticky=E+W+N+S)
        self.lb.bind('<<ListboxSelect>>',self.listselection)

        self.update()
        self.geometry(self.geometry())

        self.files_found = []

    def Onextenter(self,event):
        ext = self.entry_var3.get()
        ext = " ".join(re.findall("[a-zA-Z1-9]+", ext))
        print ext
        if ext:
            self.lb.delete(0, END)
            for files in self.files_found:
                if (files.endswith('.'+ext)):
                    self.scroll_bar(files)
        else:
            self.lb.delete(0, END)
            print self.files_found
            for files in self.files_found:
                self.scroll_bar(files)
                
    def askdirectory(self):
        self.selected_dir = tkFileDialog.askdirectory(**self.dir_opt)
        self.entry_var2.set(self.selected_dir)

    def listselection(self,evt):
        try:
            w = evt.widget
            index = int(w.curselection()[0])
            value = w.get(index)
            startfile(value)
        except IndexError:
            pass
        
    def search_file(self):
        self.files_found = []
        start = time.time()
        directory = self.entry_var2.get()
        for (dirpath, dirnames, flist) in walk(directory):
            fname = unicode(self.entry_var1.get())
            for filenames in flist:
                if fname in filenames:
                    dirpath = path.join( dirpath, '')
                    dirpath = dirpath.replace('/','\\')
                    sd_string = dirpath + filenames
                    self.files_found.append(sd_string)
                    self.scroll_bar(sd_string)
                    
        end =  time.time()
        self.label4_text.set('Time taken in secs: '+str(end - start))

    def scroll_bar(self,strings):
        self.lb.insert(END,strings)
        self.sb = Scrollbar(self,orient=VERTICAL)
        self.sb = Scrollbar(self,orient=HORIZONTAL)
        self.sb.grid(row=7,column =2,sticky = N+S+E)
        self.sb.grid(row=8,column =2,sticky = S+E+W)
        self.sb.configure(command=self.lb.yview)
        self.lb.configure(yscrollcommand=self.sb.set)

    def OnPressEnter(self,event):
        self.lb.delete(0, END)
        self.search_file()

    def OnButtonClick(self):
        self.lb.delete(0, END)
        self.search_file()

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('Python Search Utility')
    app.mainloop()
