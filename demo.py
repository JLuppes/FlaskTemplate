from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, DemoData
from datetime import datetime, timezone
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms.validators import DataRequired, Length, Regexp
from wtforms.fields import *

demo = Blueprint('demo', __name__)


class DemoForm(FlaskForm):
    dataId = HiddenField()
    demoText = StringField(
        'Demo Text', description="This is a text field", validators=[Length(0, 100)])
    demoNumber = IntegerField(
        'Demo Number', description='This is a number field')
    demoBool = BooleanField(
        'Demo Boolean', description='This is a boolean field')
    submit = SubmitField()


@demo.route('/demo', methods=['GET', 'POST'])
def demoObject():
    if request.method == 'POST':
        _method = request.form.get("_method", 'POST').strip().upper()
        if _method == 'POST' or _method == 'PUT':
            formDemoText = request.form.get("demoText", '').strip()
            formDemoNumber = request.form.get("demoNumber", '').strip()
            formDemoBool = request.form.get("demoBool", '').strip() == "true"

            if _method == 'PUT':
                formDataId = request.form.get("demoDataId", '').strip()

                if not formDataId:
                    errorMsg = "No data id provided."
                    return render_template('demoPages/admin.html', error=errorMsg)

                dataToEdit = DemoData.query.filter_by(id=formDataId).first()

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
                    redirect(url_for('demo.update'))
                except Exception as e:
                    db.session.rollback()
                    errorMsg = f"Error updating db entry with id = {formDataId}"
                    return render_template('demoPages/update/updateForm.html', error=errorMsg)

    return render_template('demo.html')


@demo.route('/demo/admin')
def admin():
    allData = DemoData.query.all()
    return render_template('demoPages/admin.html', data=allData)


@demo.route('/demo/create', methods=['GET', 'POST'])
def create():
    form = DemoForm()
    if form.validate_on_submit():
        flash('Form validated!')
        formDemoText = request.form.get("demoText", '').strip()
        formDemoNumber = request.form.get("demoNumber", '').strip()
        formDemoBool = request.form.get("demoBool", '') == "y"

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

    return render_template('demoPages/create/createForm.html', form=form)


@demo.route('/demo/read')
def read():
    return render_template('demoPages/read/read.html')


@demo.route('/demo/update', methods=['GET', 'POST'])
def update():
    form = DemoForm()

    dataId = request.args.get("dataId")

    if not dataId:
        errorMsg = "No data id provided!"
        return render_template("demo.html", error=errorMsg)

    dataToEdit = DemoData.query.filter_by(id=dataId).first()

    if not dataToEdit:
        errorMsg = f"No data found with id = {dataId}"
        return render_template("demopages/admin.html", error=errorMsg)

    if form.validate_on_submit():

        try:
            dataToEdit.demoText = form.demoText.data
            dataToEdit.demoNumber = form.demoNumber.data
            dataToEdit.demoBool = form.demoBool.data
            dataToEdit.updated = datetime.now(timezone.utc)
            db.session.commit()
            # flash(f"Successfully updated data with id: {dataId}")
            redirect(url_for('demo.admin'))
        except Exception as e:
            db.session.rollback()
            errorMsg = f"Error updating db entry with id = {dataId}. Error = {str(e)}"
            form.dataId.data = dataId
            form.demoText.data = dataToEdit.demoText
            form.demoNumber.data = dataToEdit.demoNumber
            form.demoBool.data = dataToEdit.demoBool
            return render_template('demoPages/update/updateForm.html', error=errorMsg, form=form)

    form.dataId.data = dataId
    form.demoText.data = dataToEdit.demoText
    form.demoNumber.data = dataToEdit.demoNumber
    form.demoBool.data = dataToEdit.demoBool

    return render_template('demoPages/update/updateForm.html', form=form)


@demo.route('/demo/delete', methods=['GET', 'POST', 'DELETE'])
def delete():
    if request.method == 'POST' or request.method == 'DELETE':

        dataId = request.form.get("dataId", '').strip()

        if not dataId:
            errorMsg = "No data id provided!"
            return render_template("demo.html", error=errorMsg)

        dataToDelete = DemoData.query.filter_by(id=dataId).first()

        if not dataToDelete:
            errorMsg = f"No data found with id = {dataId}"
            return render_template("demopages/admin.html", error=errorMsg)

        try:
            oldState = dataToDelete.deleted
            dataToDelete.deleted = not oldState
            db.session.commit()
            return redirect(url_for('demo.admin'))
        except Exception as e:
            db.session.rollback()
            errorMsg = f"Error deleting db entry with id = {dataId}"
            return render_template('demoPages/admin.html', error=errorMsg)

    return render_template('demoPages/admin.html')
