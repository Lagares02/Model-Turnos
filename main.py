from flask import Flask, render_template

app = Flask(__name__)

#  instanciar mi clase aqui 


# y crear rutas para solicitar el cronograma y q este se giuarde en un archivo pdf 


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
