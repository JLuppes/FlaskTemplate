from flask import Blueprint, render_template, request, redirect, url_for
from models import db, DemoData

demo = Blueprint('demo', __name__)


@demo.route('/demo')
def crudPage():
    return render_template('demo.html')


@demo.route('/demo/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':

        formDemoText = request.form.get("demoText", '').strip()
        formDemoNumber = request.form.get("demoNumber", '').strip()
        formDemoBool = request.form.get("demoBool", '').strip() == "true"

        try:
            newDemoData = DemoData(
                demoText=formDemoText,
                demoNumber=formDemoNumber,
                demoBool=formDemoBool
            )
            db.session.add(newDemoData)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            errorMsg = f"Error during database operation: {str(e)}"
            return render_template('demoPages/create/createForm.html', error=errorMsg)

        freshDemoData = DemoData.query.filter(
            DemoData.demoText == formDemoText, DemoData.demoNumber == formDemoNumber, DemoData.demoBool == formDemoBool).first()

        return render_template('demoPages/create/createSuccess.html', demoData=freshDemoData)

    return render_template('demoPages/create/createForm.html')


@demo.route('/demo/read')
def read():
    return render_template('demoPages/read/read.html')


@demo.route('/demo/update')
def update():
    return render_template('demoPages/update/update.html')


@demo.route('/demo/delete')
def delete():
    return render_template('demoPages/delete/delete.html')
