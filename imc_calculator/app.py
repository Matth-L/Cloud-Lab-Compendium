from flask import Flask, request, redirect, render_template

app = Flask(__name__)

def calculate_bmi(weight, height):
    return round(weight / (height ** 2), 2)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        weight = float(request.form.get('weight'))
        height = float(request.form.get('height'))
        bmi = calculate_bmi(weight, height)
        # Rediriger vers une route locale avec l'IMC en paramètre
        return redirect(f'/result?bmi={bmi}')
    return render_template('index.html')

@app.route('/result')
def result():
    bmi = request.args.get('bmi')
    return render_template('result.html', bmi=bmi)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
