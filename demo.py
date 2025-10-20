from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, DemoData
from datetime import datetime, timezone

demo = Blueprint('demo', __name__)


@demo.route('/demo', methods=['GET', 'POST'])
def demoObject():
    if request.method == 'POST':
        _method = request.form.get("_method", 'POST').strip().upper()
        if _method == 'POST' or _method == 'PUT':
            formDemoText = request.form.get("demoText", '').strip()
            formDemoNumber = request.form.get("demoNumber", '').strip()
            formDemoBool = request.form.get("demoBool", '').strip() == "true"

            if _method == 'POST':

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
            elif _method == 'PUT':
                formDataId = request.form.get("demoId", '').strip()

                if not formDataId:
                    errorMsg = "No data id provided."
                    return render_template('demoPages/update/updateForm.html', error=errorMsg)

                dataToEdit = DemoData.query.filter_by(id=formDataId)

                if not dataToEdit:
                    errorMsg = f"No data found with id = {formDataId}"
                    return render_template('demoPages/update/updateForm.html', error=errorMsg)

                try:
                    dataToEdit.demoText = formDemoText
                    dataToEdit.demoNumber = formDemoNumber
                    dataToEdit.demoBool = formDemoBool
                    dataToEdit.updated = datetime.now(timezone.utc)
                    db.session.commit()
                    flash(f"Successfully updated data with id: {formDataId}")
                    redirect(url_for('update'))
                except Exception as e:
                    db.session.rollback()
                    errorMsg = f"Error updating db entry with id = {formDataId}"
                    return render_template('demoPages/update/updateForm.html', error=errorMsg)

    return render_template('demo.html')


@demo.route('/demo/admin')
def admin():
    allData = DemoData.query.all()
    return render_template('demoPages/admin.html', data=allData)


@demo.route('/demo/create')
def create():
    return render_template('demoPages/create/createForm.html')


@demo.route('/demo/read')
def read():
    return render_template('demoPages/read/read.html')


@demo.route('/demo/update')
def update():
    dataId = request.args.get("dataId", '').strip()

    if not dataId:
        errorMsg = "No data id provided!"
        return render_template("demo.html", error=errorMsg)

    dataToEdit = DemoData.query.filter_by(id=dataId).first()
    if not dataToEdit:
        errorMsg = f"No data found with id = {dataId}"
        return render_template("demopages/demo.html", error=errorMsg)

    return render_template('demoPages/update/updateForm.html', data=dataToEdit)


@demo.route('/demo/delete')
def delete():
    return render_template('demoPages/delete/delete.html')
