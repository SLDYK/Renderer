# -*- coding: utf-8 -*-
import tkinter
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import zipfile
import os
import traceback
from RendererUI import renderer


def settings_fix(filePath):
    with open(filePath,"r",encoding="utf_8") as t:
        chartdata=t.readlines()
        t.close()
    with open(filePath,"w",encoding="utf_8") as t:
        for i in range(len(chartdata)):
            if i<=9:
                t.write(chartdata[i])
            else:
                if "#" in chartdata[i]:
                    t.write(chartdata[i])
                    t.write(chartdata[i+1])
                    t.write(chartdata[i+2])
                    t.write(chartdata[i+3])
                    t.write(chartdata[i+4])
                    t.write(chartdata[i+5])
                    t.write(chartdata[i+6])
                    t.write(chartdata[i+7])
                    if len(chartdata)>=i+8:
                        if "Painter: " in chartdata[i+8]:
                            t.write(chartdata[i+8])
                            t.write("\n")
                        else:
                            t.write("Painter: 无信息\n\n")
                    else:
                        t.write("Painter: 无信息\n\n")
        t.close()     

def load():
    try:
        with open("PEdata","r",encoding="utf_8") as p:
            PEdata=p.read()
            p.close()
        settings_fix(PEdata+"Settings.txt")
        with open(PEdata+"Settings.txt","r",encoding="utf_8") as t:
            chartdata=t.readlines()
            t.close()
        #global table
        elem=table.get_children()
        for item in elem:
            table.delete(item)
        j=0
        for i in range(0,len(chartdata)):
            if chartdata[i]=="#\n":
                table.insert("",j,values=(chartdata[i+1][6:-1],
                                          chartdata[i+2][6:-1],
                                          chartdata[i+3][9:-1],
                                          chartdata[i+4][7:-1],
                                          chartdata[i+5][7:-1],
                                          chartdata[i+6][10:-1],
                                          chartdata[i+7][9:-1],
                                          chartdata[i+8][9:-1]))
    except:
        with open("ErrorsLog.txt","a",encoding="utf_8") as t:
            traceback.print_exc(file=t)
            t.close()
        messagebox.showinfo("绑定PE","首次运行时请绑定您的PhiEditer")
        PEPath=filedialog.askopenfilename(initialfile="PhiEditer.exe",filetypes=[('PhiEditer','.exe')])
        with open("PEdata","w",encoding="utf_8") as t:
            t.write(PEPath.replace("PhiEditer.exe",""))
            t.close()
        load()
        
def importchart():
    try:
        with open("PEdata","r",encoding="utf_8") as p:
            PEdata=p.read()
            p.close()
    except:
        pass
    picture=["png","jpg","jpeg"]
    music=["mp3","wav","ogg","flac"]
    filePath=filedialog.askopenfilename(filetypes=[('PE谱面','.zip')])
    fz=zipfile.ZipFile(filePath,"r")
    level="无信息"
    composer="无信息"
    charter="无信息"
    painter="无信息"
    name=filePath.split("/")[-1].replace(".zip","")
    for file in fz.namelist():
        if file.split(".")[-1]=="pec":
            fz.extract(file,PEdata)
            chart=file
        elif file.split(".")[-1] in music:
            fz.extract(file,PEdata+"Resources/")
            music=file
        elif file.split(".")[-1] in picture:
            fz.extract(file,PEdata+"Resources/")
            picture=file
    for file in fz.namelist():
        if file=="Settings.txt":
            fz.extract(file,"infodir/")
            with open("infodir/settings.txt","r",encoding="utf_8") as t:
                data=t.readlines()
                for i in range(len(data)):
                    if "Level: " in data[i]:
                        level=data[i][7:-1]
                    elif "Charter: " in data[i]:
                        charter=data[i][9:-1]
                    elif "Composer: " in data[i]:
                        composer=data[i][10:-1]
                    elif "Painter: " in data[i]:
                        painter=data[i][9:-1]
                    elif "Name: " in data[i]:
                        name=data[i][6:-1]
                t.close()
            os.remove("infodir/settings.txt")
            os.rmdir("infodir")
            break
        elif file=="info.csv":
            fz.extract(file,"infodir/")
            with open("infodir/info.csv","r",encoding="utf_8") as t:
                data=t.readlines()
                for i in range(len(data)):
                    if "Name" in data[i]:
                        title=data[i].replace("\n","").split(",")
                value=data[-1].replace("\n","").split(",")
                try:
                    level=value[title.index("Level")]
                except:
                    pass
                try:
                    charter=value[title.index("Charter")]
                except:
                    pass
                try:
                    composer=value[title.index("Artist")]
                except:
                    pass
                try:
                    painter=value[title.index("Illustrator")]
                except:
                    pass
                try:
                    name=value[title.index("Name")]
                except:
                    pass
                t.close()
            os.remove("infodir/info.csv")
            os.rmdir("infodir")
    fz.close()
    with open(PEdata+"Settings.txt","a",encoding="utf_8") as t:
        info=("\n#\nName: "+name+
              "\nSong: "+music+
              "\nPicture: "+picture+
              "\nChart: "+chart+
              "\nLevel: "+level+
              "\nComposer: "+composer+
              "\nCharter: "+charter+
              "\nPainter: "+painter+
              "\n")
        t.write(info)
        t.close()
    messagebox.showinfo("Succes","成功导入谱面")
    load()

def exportchart(item):
    try:
        with open("PEdata","r",encoding="utf_8") as p:
            PEdata=p.read()
            p.close()
    except:
        pass
    def infocsv(infolist):
        setinfo.destroy()
        item=infolist[8]
        savePath=filedialog.asksaveasfilename(initialfile=item[0]+'.zip',filetypes=[("PE谱面", ".zip")])
        with open("infodata","w",encoding="utf_8") as t:
            t.write("Chart,Music,Image,Name,Artist,Level,Illustrator,Charter\n谱面,音乐,图片,名称,曲师,等级,曲绘,谱师\n")
            t.write(infolist[0]+","+infolist[1]+","+infolist[2]+","+infolist[3]+","+infolist[4]+","+infolist[5]+","+infolist[6]+","+infolist[7])
            t.close()
        with open("settingsdata","w",encoding="utf_8") as t:
            t.write("\n#\nName: "+infolist[3]+
                  "\nSong: "+infolist[1]+
                  "\nPicture: "+infolist[2]+
                  "\nChart: "+infolist[0]+
                  "\nLevel: "+infolist[5]+
                  "\nComposer: "+infolist[4]+
                  "\nCharter: "+infolist[7]+
                  "\nPainter: "+infolist[6]+
                  "\n")
            t.close()
        z=zipfile.ZipFile(savePath,"w",zipfile.ZIP_DEFLATED)
        z.write(PEdata+item[3],item[3])
        z.write(PEdata+"Resources/"+item[1],item[1])
        z.write(PEdata+"Resources/"+item[2],item[2])
        z.write("infodata","info.csv")
        z.write("settingsdata","Settings.txt")
        z.close()
        os.remove("infodata")
        os.remove("settingsdata")
        messagebox.showinfo("Succes","成功导出谱面")
        
    holdon=False
    #global table
    if item=="":
        messagebox.showinfo("Error","未选择谱面")
    else:
        info=messagebox.askyesno("Export","是否生成info.csv和settings.txt")
        if info:
            setinfo=tkinter.Toplevel()
            setinfo.title("填写谱面信息")
            setinfo.geometry("300x300")
            subtitle=tkinter.Label(setinfo, text="填写谱面信息",font=('', 10),width=30,height=1)
            subtitle.place(relx=0.5,rely=0.1,anchor=tkinter.CENTER)
            
            name=tkinter.Label(setinfo, text='名称:',font=('',10),width=30,height=1)
            name.place(relx=0.15,rely=0.19,anchor=tkinter.CENTER)
            enname=tkinter.Entry(setinfo,show=None,width=25)
            enname.insert(0,item[0])
            enname.place(relx=0.52,rely=0.19,anchor=tkinter.CENTER)

            music=tkinter.Label(setinfo, text='音频:',font=('',10),width=30,height=1)
            music.place(relx=0.15,rely=0.28,anchor=tkinter.CENTER)
            enmusic=tkinter.Entry(setinfo,show=None,width=25)
            enmusic.insert(0,item[1])
            enmusic.place(relx=0.52,rely=0.28,anchor=tkinter.CENTER)

            photo=tkinter.Label(setinfo, text='背景:',font=('',10),width=30,height=1)
            photo.place(relx=0.15,rely=0.37,anchor=tkinter.CENTER)
            enphoto=tkinter.Entry(setinfo,show=None,width=25)
            enphoto.insert(0,item[2])
            enphoto.place(relx=0.52,rely=0.37,anchor=tkinter.CENTER)

            chart=tkinter.Label(setinfo, text='谱面:',font=('',10),width=30,height=1)
            chart.place(relx=0.15,rely=0.46,anchor=tkinter.CENTER)
            enchart=tkinter.Entry(setinfo,show=None,width=25)
            enchart.insert(0,item[3])
            enchart.place(relx=0.52,rely=0.46,anchor=tkinter.CENTER)

            level=tkinter.Label(setinfo, text='难度:',font=('',10),width=30,height=1)
            level.place(relx=0.15,rely=0.55,anchor=tkinter.CENTER)
            enlevel=tkinter.Entry(setinfo,show=None,width=25)
            enlevel.insert(0,item[4])
            enlevel.place(relx=0.52,rely=0.55,anchor=tkinter.CENTER)

            composer=tkinter.Label(setinfo, text='曲师:',font=('',10),width=30,height=1)
            composer.place(relx=0.15,rely=0.64,anchor=tkinter.CENTER)
            encomposer=tkinter.Entry(setinfo,show=None,width=25)
            encomposer.insert(0,item[5])
            encomposer.place(relx=0.52,rely=0.64,anchor=tkinter.CENTER)

            charter=tkinter.Label(setinfo, text='谱师:',font=('',10),width=30,height=1)
            charter.place(relx=0.15,rely=0.73,anchor=tkinter.CENTER)
            encharter=tkinter.Entry(setinfo,show=None,width=25)
            encharter.insert(0,item[6])
            encharter.place(relx=0.52,rely=0.73,anchor=tkinter.CENTER)

            illustrator=tkinter.Label(setinfo, text='画师:',font=('',10),width=30,height=1)
            illustrator.place(relx=0.15,rely=0.82,anchor=tkinter.CENTER)
            enillustrator=tkinter.Entry(setinfo,show=None,width=25)
            enillustrator.insert(0,item[7])
            enillustrator.place(relx=0.52,rely=0.82,anchor=tkinter.CENTER)

            done=tkinter.Button(setinfo,text='下一步',font=('',10),width=10,height=1,command=lambda:infocsv([enchart.get(),enmusic.get(),enphoto.get(),enname.get(),encomposer.get(),enlevel.get(),enillustrator.get(),encharter.get(),item]))
            done.place(relx=0.5,rely=0.92,anchor=tkinter.CENTER)
            setinfo.mainloop()
        else:
            holdon=True
        if holdon:
            savePath=filedialog.asksaveasfilename(initialfile=item[0]+'.zip',filetypes=[("PE谱面", ".zip")])    
            z=zipfile.ZipFile(savePath,"w",zipfile.ZIP_DEFLATED)
            z.write(item[3],item[3])
            z.write("Resources/"+item[1],item[1])
            z.write("Resources/"+item[2],item[2])
            z.close()
            messagebox.showinfo("Succes","成功导出谱面")

def deletechart(item):
    #global table
    try:
        with open("PEdata","r",encoding="utf_8") as p:
            PEdata=p.read()
            p.close()
    except:
        pass
    if item=="":
        messagebox.showinfo("Error","未选择谱面")
    else:
        result=messagebox.askyesno("Delete","是否删除谱面")
        if result:
            info="\n#\nName: "+item[0]+"\nSong: "+item[1]+"\nPicture: "+item[2]+"\nChart: "+item[3]+"\nLevel: "+item[4]+"\nComposer: "+item[5]+"\nCharter: "+item[6]+"\nPainter: "+item[7]
            with open(PEdata+"Settings.txt","r",encoding="utf_8") as t:
                basicset=t.read()
                t.close()
            with open(PEdata+"Settings.txt","w",encoding="utf_8") as t:
                t.write(basicset.replace(info,""))
                t.close()
            with open(PEdata+"Settings.txt","r",encoding="utf_8") as t:
                chartdata=t.readlines()
                t.close()
            undeleted=[]
            for i in range(len(chartdata)):
                if chartdata[i]=="#\n":
                    undeleted.append(chartdata[i+2][6:-1])
                    undeleted.append(chartdata[i+3][9:-1])
                    undeleted.append(chartdata[i+4][7:-1])
            if item[3] not in undeleted:
                os.remove(PEdata+item[3])
            if item[1] not in undeleted:
                os.remove(PEdata+"Resources/"+item[1])
            if item[2] not in undeleted:
                os.remove(PEdata+"Resources/"+item[2])
            messagebox.showinfo("Success","已删除谱面 "+item[0])
        load()

def editinfo(item):
    
    def newinfo(infolist):
        setinfo.destroy()
        info=("#\nName: "+infolist[3]+
              "\nSong: "+infolist[1]+
              "\nPicture: "+infolist[2]+
              "\nChart: "+infolist[0]+
              "\nLevel: "+infolist[5]+
              "\nComposer: "+infolist[4]+
              "\nCharter: "+infolist[7]+
              "\nPainter: "+infolist[6])
        try:
            with open("PEdata","r",encoding="utf_8") as p:
                PEdata=p.read()
                p.close()
        except:
            pass
        
        with open(PEdata+"Settings.txt","r",encoding="utf_8") as t:
            settings=t.read()
            t.close()
        with open(PEdata+"Settings.txt","w",encoding="utf_8") as t:
            t.write(settings.replace(infolist[8],info))
            t.close()
        load()
    
    oldinfo=("#\nName: "+item[0]+
            "\nSong: "+item[1]+
            "\nPicture: "+item[2]+
            "\nChart: "+item[3]+
            "\nLevel: "+item[4]+
            "\nComposer: "+item[5]+
            "\nCharter: "+item[6]+
            "\nPainter: "+item[7])
    
    setinfo=tkinter.Toplevel()
    setinfo.title("编辑谱面信息")
    setinfo.geometry("300x300")
    subtitle=tkinter.Label(setinfo, text="编辑谱面信息",font=('', 10),width=30,height=1)
    subtitle.place(relx=0.5,rely=0.1,anchor=tkinter.CENTER)
    
    name=tkinter.Label(setinfo, text='名称:',font=('',10),width=30,height=1)
    name.place(relx=0.15,rely=0.19,anchor=tkinter.CENTER)
    enname=tkinter.Entry(setinfo,show=None,width=25)
    enname.insert(0,item[0])
    enname.place(relx=0.52,rely=0.19,anchor=tkinter.CENTER)

    music=tkinter.Label(setinfo, text='音频:',font=('',10),width=30,height=1)
    music.place(relx=0.15,rely=0.28,anchor=tkinter.CENTER)
    enmusic=tkinter.Entry(setinfo,show=None,width=25)
    enmusic.insert(0,item[1])
    enmusic.place(relx=0.52,rely=0.28,anchor=tkinter.CENTER)

    photo=tkinter.Label(setinfo, text='背景:',font=('',10),width=30,height=1)
    photo.place(relx=0.15,rely=0.37,anchor=tkinter.CENTER)
    enphoto=tkinter.Entry(setinfo,show=None,width=25)
    enphoto.insert(0,item[2])
    enphoto.place(relx=0.52,rely=0.37,anchor=tkinter.CENTER)

    chart=tkinter.Label(setinfo, text='谱面:',font=('',10),width=30,height=1)
    chart.place(relx=0.15,rely=0.46,anchor=tkinter.CENTER)
    enchart=tkinter.Entry(setinfo,show=None,width=25)
    enchart.insert(0,item[3])
    enchart.place(relx=0.52,rely=0.46,anchor=tkinter.CENTER)

    level=tkinter.Label(setinfo, text='难度:',font=('',10),width=30,height=1)
    level.place(relx=0.15,rely=0.55,anchor=tkinter.CENTER)
    enlevel=tkinter.Entry(setinfo,show=None,width=25)
    enlevel.insert(0,item[4])
    enlevel.place(relx=0.52,rely=0.55,anchor=tkinter.CENTER)

    composer=tkinter.Label(setinfo, text='曲师:',font=('',10),width=30,height=1)
    composer.place(relx=0.15,rely=0.64,anchor=tkinter.CENTER)
    encomposer=tkinter.Entry(setinfo,show=None,width=25)
    encomposer.insert(0,item[5])
    encomposer.place(relx=0.52,rely=0.64,anchor=tkinter.CENTER)

    charter=tkinter.Label(setinfo, text='谱师:',font=('',10),width=30,height=1)
    charter.place(relx=0.15,rely=0.73,anchor=tkinter.CENTER)
    encharter=tkinter.Entry(setinfo,show=None,width=25)
    encharter.insert(0,item[6])
    encharter.place(relx=0.52,rely=0.73,anchor=tkinter.CENTER)

    illustrator=tkinter.Label(setinfo, text='画师:',font=('',10),width=30,height=1)
    illustrator.place(relx=0.15,rely=0.82,anchor=tkinter.CENTER)
    enillustrator=tkinter.Entry(setinfo,show=None,width=25)
    enillustrator.insert(0,item[7])
    enillustrator.place(relx=0.52,rely=0.82,anchor=tkinter.CENTER)

    done=tkinter.Button(setinfo,text='确认修改',font=('',10),width=10,height=1,command=lambda:newinfo([enchart.get(),enmusic.get(),enphoto.get(),enname.get(),encomposer.get(),enlevel.get(),enillustrator.get(),encharter.get(),oldinfo]))
    done.place(relx=0.5,rely=0.92,anchor=tkinter.CENTER)
    setinfo.mainloop()
    

root=tkinter.Tk()
root.title("PERenderer Manager 0.3.0")
root.geometry("615x300")
b1=tkinter.Button(root,text='导入谱面',font=('',10),width=8,height=2,command=importchart)
b1.place(relx=0.077,rely=0.1,anchor=tkinter.CENTER)
b2=tkinter.Button(root,text='导出谱面',font=('',10),width=8,height=2,command=lambda:exportchart(table.item(table.selection(),"values")))
b2.place(relx=0.197,rely=0.1,anchor=tkinter.CENTER)
b3=tkinter.Button(root,text='删除谱面',font=('',10),width=8,height=2,command=lambda:deletechart(table.item(table.selection(),"values")))
b3.place(relx=0.317,rely=0.1,anchor=tkinter.CENTER)
b4=tkinter.Button(root,text='编辑信息',font=('',10),width=8,height=2,command=lambda:editinfo(table.item(table.selection(),"values")))
b4.place(relx=0.437,rely=0.1,anchor=tkinter.CENTER)
b5=tkinter.Button(root,text='视频渲染',font=('',10),width=8,height=2,command=lambda:renderer(table.item(table.selection(),"values")))
b5.place(relx=0.557,rely=0.1,anchor=tkinter.CENTER)
b6=tkinter.Button(root,text='加载数据',font=('',10),width=8,height=2,command=load)
b6.place(relx=0.885,rely=0.1,anchor=tkinter.CENTER)
table=ttk.Treeview(root,columns=("名称","音频","背景","谱面","难度","曲师","谱师","画师"),show="headings")
table.column("名称",width=70)
table.column("音频",width=70)
table.column("背景",width=70)
table.column("谱面",width=70)
table.column("难度",width=70)
table.column("曲师",width=70)
table.column("谱师",width=70)
table.column("画师",width=70)
table.heading("名称",text="名称")
table.heading("音频",text="音频")
table.heading("背景",text="背景")
table.heading("谱面",text="谱面")
table.heading("难度",text="难度")
table.heading("曲师",text="曲师")
table.heading("谱师",text="谱师")
table.heading("画师",text="画师")
table.place(relx=0.48,rely=0.57,anchor=tkinter.CENTER)
ybar=ttk.Scrollbar(root,orient="vertical",command=table.yview)
table["yscroll"]=ybar.set
ybar.place(relx=0.96,rely=0.3,anchor=tkinter.CENTER)
root.mainloop()