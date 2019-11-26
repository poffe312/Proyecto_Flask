
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
import io
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import base64

app = Flask(__name__)

app.config["CSV"] = "./static/csv"

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/columnas', methods=['POST'])
def columnas():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config["CSV"], filename))

        df = pd.read_csv('./static/csv/{}'.format(filename))

        print(df.columns.tolist())
        columnas = { 
            'columnas': df.columns.tolist(),
            'filename': filename
        }
        return render_template('graficar.html', columnas=columnas)

@app.route('/graficar', methods=['POST'])
def graficar():
    if request.method == 'POST':
        columna = request.form['columna']
        tipo = request.form['tipo']
        nombre = request.form['nombre']
        filename = request.form['filename']

        df = pd.read_csv('./static/csv/{}'.format(filename))[columna]

        plt.clf() 
        if tipo == 'puntos':
            img = io.BytesIO()
            plt.title(nombre)
            plt.plot(df.head(10),'--')
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return render_template('grafica.html', imagen={ 'imagen': plot_url })
        elif tipo == 'lineas':
            print('lineas')
            img = io.BytesIO()
            plt.title(nombre)
            plt.plot(df.head(10))
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return render_template('grafica.html', imagen={ 'imagen': plot_url })
        elif tipo == 'pastel':
            img = io.BytesIO()
            plt.title(nombre)
            datos = df.head(10).tolist()
            plt.pie(datos, autopct="%0.1f %%")
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return render_template('grafica.html', imagen={ 'imagen': plot_url })
        else:
            img = io.BytesIO()
            plt.title(nombre)
            datos = df.head(10).tolist()
            for i in range(len(datos)):
                plt.bar(i, datos[i], align = 'center')
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return render_template('grafica.html', imagen={ 'imagen': plot_url })

@app.errorhandler(404)
def page_not_found(error):
    return '<h1>Pagina no encontrada</h1>'

if __name__ == "__main__":
    app.run(port = 80, debug = True)