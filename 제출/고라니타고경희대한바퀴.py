#1) 값을 받음
#----------------------------------------------------------
import resources
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

class InputDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("main.ui", self)  # UI 파일 로드
        self.pushButton.clicked.connect(self.on_button_click)

    def on_button_click(self):
        global what
        global address
        what = self.textEdit.toPlainText()  # 첫 번째 QTextEdit의 텍스트를 가져옴
        address = self.textEdit_2.toPlainText()  # 두 번째 QTextEdit의 텍스트를 가져옴

        print("상품명:", what)
        print("배송지:", address)

        self.a = what  # 첫 번째 변수에 저장
        self.b = address  # 두 번째 변수에 저장
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InputDialog()
    window.show()
    app.exec_()

#2 도로명을 좌표로 전환--------------------------------------------------------------------
import googlemaps

def change_address(api_key, address):
    gmaps = googlemaps.Client(key=api_key)
    result = gmaps.geocode(address, region='kr')  # region='kr'을 추가하여 한국 내의 주소로 제한
    if result:
        location = result[0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        print("주소를 찾을 수 없습니다.")
        return None, None

api_key = "AIzaSyAYvTJludX6hqNVwjzj5XbJ2JY9m57fnLY"

latitude, longitude = change_address(api_key, address)
if latitude is not None and longitude is not None:
        print(f"도로명 주소 '{address}'의 좌표는 위도 {latitude}, 경도 {longitude} 입니다.")
else:
        print("해당 주소의 좌표를 찾을 수 없습니다.")

#3)가장 거리가 짧은 place어디?----------------------------------------------------------------------


import pandas as pd 

data = pd.read_excel('juso.xlsx') 

wido_data = list(data["위도"])
gungdo_data = list(data["경도"])
wido_data2 = list(data["집하장 위도"])
gungdo_data2 = list(data["집하장 경도"])

result = []

#---------------------------------------
import pandas as pd
from openpyxl import load_workbook

# 거리 계산 및 결과 저장
for i in range(0, len(wido_data)):
    re = ((wido_data[i] - wido_data2[i])**2 + (gungdo_data[i] - gungdo_data2[i])**2)**0.5
    re += (((latitude - wido_data2[i])**2 + (longitude - gungdo_data2[i])**2)**0.5)
    result.append(re)

# 엑셀 파일에서 상품명 정보 가져오기
wb = load_workbook("juso.xlsx")
dd = wb.active
low_co2 = []

# 최소 거리를 가진 상품명과 거리 정보를 low_co2 리스트에 저장
for i in range(len(result)):
    a = result[i]
    x = result.index(a) + 1
    low_co2.append([dd["A%d" % x].value,  result[i],dd["H%d" %x].value])

# DataFrame으로 변환
col = ['상품명', "거리","사이트"]
df = pd.DataFrame(data=low_co2, columns=col)
df2=df.sort_values(by='거리',ascending=True)

# 'what' 변수와 일치하는 행의 '거리' 열 값을 추출하여 리스트로 만듦
site_list = df2.loc[df2['상품명'] == what, '사이트'].tolist()
#for i in range(len(site_list)):
#    print(i+1,site_list[i],"\n")



#4) 출력
import tkinter as tk
from PIL import ImageTk, Image

def show_result(L):
    
    rank_text = '\n'.join(map(str, L))

    root = tk.Tk()
    root.title("탄소발자국을 줄여보아용")

    # 텍스트 추가
    ranK_co2 = tk.Text(root, wrap=tk.WORD,font=("Arial", 12)) # width=40, height=10, font=("Arial", 12)
    ranK_co2.insert(tk.INSERT, rank_text)
    ranK_co2.pack()

    root.mainloop()

# 예시 리스트

show_result(site_list)