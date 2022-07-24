import os, cv2
import tkinter as tk
import tkinter.filedialog
import matplotlib.pyplot as plt

class TkinterClass(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.pack()
        # self.pack_propagate(0)

        button = tk.Button(root, text='1. ファイルを参照')
        button.bind('<ButtonPress>', self.file_dialog)
        button.pack()

        self.file_name = tk.StringVar()
        self.file_name.set('未選択です')
        label = tk.Label(textvariable=self.file_name,)
        label.pack()

        self.isImgSelect = False
        self.img_data = []
        self.imgs = tk.StringVar()
        self.imgs.set('画像が選択されていません')
        label = tk.Label(textvariable=self.imgs)
        label.pack()

        stitch_button = tk.Button(root, text='2. 重ね合わせる' ,command=self.isStitch)
        stitch_button.bind('<ButtonPress>', self.stitch)
        stitch_button.pack()

        self.process = tk.StringVar()
        self.isProcess = False
        self.process.set('')
        label = tk.Label(textvariable=self.process)
        label.pack()
        
        self.result = tk.StringVar()
        self.result.set('')
        label = tk.Label(textvariable=self.result)
        label.pack()

        self.img_result = []
        save_button = tk.Button(root, text='3. 保存する')
        save_button.bind('<ButtonPress>', self.save)
        save_button.pack()

        self.end = tk.StringVar()
        self.end.set('')
        label = tk.Label(textvariable=self.end)
        label.pack()

        clear_button = tk.Button(root, text='やり直す')
        clear_button.bind('<ButtonPress>', self.clear)
        clear_button.pack(side=tk.BOTTOM,pady=10)
    
    def file_dialog(self, event):
        fTyp = [("",'.jpg .tiff .png')]
        iDir = os.path.abspath(os.path.dirname(__file__))
        file_name = tk.filedialog.askopenfilenames(filetypes=fTyp, initialdir=iDir, title='写真を選ぶ')
        file_name = list(file_name)
        if len(file_name) == 0:
            self.file_name.set('選択をキャンセルしました')
        else:
            self.file_name.set('')
            self.img_data = file_name
            self.imgs.set(str(len(file_name))+'枚の写真が読み込まれました')
            self.isImgSelect = True

    def isStitch(self):
        self.process.set('処理中です')
        self.isProcess = True

    def stitch(self, event):
        if self.isImgSelect:
            self.process.set('処理中です')
            print('処理中です.')
            img_data = self.img_data
            read_img = []
            for i in img_data:
                read_img.append(cv2.imread(i))

            stitcher = cv2.Stitcher.create(mode=cv2.Stitcher_SCANS)
            result = stitcher.stitch(read_img)
            if result[0]==0:
                self.img_result = result
                self.result.set('重ね合わせに成功しました')
                img_r = cv2.cvtColor(result[1], cv2.COLOR_BGR2RGB)
                plt.imshow(img_r)
                plt.show()
            elif result[0]==1:
                self.result.set('重ね合わせに失敗しました')
            self.isProcess = False
            print('処理完了.確認して保存')
    
    def save(self, event):
        if self.img_result != []:
            iDir = os.path.abspath(os.path.dirname(__file__))
            fname = tkinter.filedialog.asksaveasfilename(
                title = "名前を付けて保存",
                filetypes = [("JPEG", ".jpg"), ("Bitmap", ".bmp"), ("PNG", ".png"), ("Tiff", ".tif") ], # ファイルフィルタ
                initialdir = iDir # 自分自身のディレクトリ
                # defaultextension = "jpg"
            )
            if fname:
                cv2.imwrite(fname, self.img_result[1])
                self.end.set('保存が完了しました')
            else:
                self.end.set('キャンセルしました')
    
    def clear(self, event):
        self.file_name.set('未選択です')
        self.isImgSelect = False
        self.img_data = []
        self.imgs.set('画像が選択されていません')
        self.process.set('') 
        self.result.set('')
        self.img_result = []
        self.end.set('')
 

if __name__ == ('__main__'):
    root = tk.Tk()
    root.geometry("360x240")
    root.title('Photo Stitcher')
    app = TkinterClass(root=root)
    app.mainloop()  