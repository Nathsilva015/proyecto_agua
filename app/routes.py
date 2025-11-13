import csv
from flask import Response
from flask import render_template, request, redirect, url_for
from app import db
from app.models import RegistroAgua
from flask_mail import Mail, Message

mail = Mail()

def init_routes(app):
    mail.init_app(app)

    @app.route('/')
    def index():
        registros = RegistroAgua.query.all()
        return render_template('index.html', registros=registros)

    @app.route('/registro', methods=['GET', 'POST'])
    def registro():
        if request.method == 'POST':
            captada = float(request.form['captada'])
            consumida = float(request.form['consumida'])
            observaciones = request.form['observaciones']

            nuevo = RegistroAgua(captada=captada, consumida=consumida, observaciones=observaciones)
            db.session.add(nuevo)
            db.session.commit()
            return redirect(url_for('index'))

        return render_template('registro.html')
    
    @app.route('/enviar_alerta')
    def enviar_alerta():
        msg = Message(
            "Alerta de Agua 💧",
            sender=app.config['MAIL_USERNAME'],
            recipients=["destinatario@gmail.com"],  # 👈 cámbialo por tu correo real
            body="El tanque de agua está casi vacío. Por favor revisa el sistema."
        )
        mail.send(msg)
        return "Correo enviado con éxito ✅"
    
    @app.route('/exportar_csv')
    def exportar_csv():
        registros = RegistroAgua.query.all()
        output = []
        for r in registros:
            output.append([r.fecha, r.captada, r.consumida, r.observaciones])
        si = []
        si.append(['Fecha', 'Captada', 'Consumida', 'Observaciones'])
        si.extend(output)

        # Genera el contenido del CSV
        def generate():
            for row in si:
                yield ','.join(map(str, row)) + '\n'

        return Response(generate(),
                        mimetype='text/csv',
                        headers={'Content-Disposition': 'attachment;filename=registros.csv'})    