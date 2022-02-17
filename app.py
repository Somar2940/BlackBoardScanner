from flask import Flask, render_template, request, redirect, url_for
import glob
import re
import os

app = Flask(__name__)

# imgfileのsort
# edit in local
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

@app.route('/', methods=['GET', 'POST'])
def index():
   if request.method == 'POST':
      grade = request.form.get('grade')
      classroom = request.form.get('classroom')
      capDate = request.form.get('date')

      if grade == "-" or classroom == "-" or capDate == '':
         return render_template('index.html')

      else:
         #文字列整形
         grade = grade.replace('年','grade')
         classroom = classroom.replace('組','class')
         capDate = capDate.replace('年','').replace('月','').replace('日','')

         return redirect(url_for("watch", grade=grade, classroom=classroom, capDate=capDate))

   else:
      return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
   if request.method == 'GET':
      return render_template('admin/admin.html')
   else:
      if request.form['send'] == 'vertex':
         return redirect(url_for("index"))

'''
@app.route('/<string:imgBaseName>', methods=['GET'])
def watch(imgBaseName):
   imgfiles = [os.path.basename(r) for r in sorted(glob.glob('static/mainImg/' + imgBaseName + '*.jpg'), key=natural_keys)]
   return render_template('watch.html',imgfiles = imgfiles)
'''

@app.route('/<string:capDate>/<string:grade>/<string:classroom>', methods=['GET'])
def watch(grade, classroom, capDate):
   grade = grade.replace('grade','')
   classroom = classroom.replace('class','')

   # 画像検索
   imgURL = str(capDate) + "/" + str(grade) + "/" + str(classroom)
   imgfiles_left = ["left/" + os.path.basename(r) for r in sorted(glob.glob('static/mainImg/' + imgURL + '/left/*.png'), key=natural_keys)]
   imgfiles_right = ["right/" + os.path.basename(r) for r in sorted(glob.glob('static/mainImg/' + imgURL + '/right/*.png'), key=natural_keys)]
   imgfiles = [None]*(len(imgfiles_left)+len(imgfiles_right))
   imgfiles[::2] = imgfiles_left
   imgfiles[1::2] = imgfiles_right

   # 教室名作成
   if classroom.isdecimal():
      GradeAndClass = str(grade) + "-" + str(classroom)
   else:
      GradeAndClass = str(classroom) + str(grade)

   # 日付作成
   str_capDate = capDate[:4] + "年" + capDate[4:6] + "月" + capDate[6:] + "日"

   return render_template('watch.html', imgfiles=imgfiles, imgURL=imgURL, GradeAndClass=GradeAndClass, capDate=str_capDate)

@app.route('/vertexSetting', methods=['GET', 'POST'])
def vertex():
   if request.method == 'GET':
      return render_template('index.html')

# メイン関数
if __name__ == "__main__":
    app.run("127.0.0.1", debug=True)
