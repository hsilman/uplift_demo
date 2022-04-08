from flask import Flask, render_template, request, jsonify
import json


with open('static/providers.json', encoding='utf8') as d:
    data = json.load(d)

for i in data:
    i['times_seen'] = 0

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('providers.html', title="page", result=data)


@app.route("/search", methods=['POST'])
def search():
    firstName = request.form['First Name']
    lastName = request.form['Last Name']
    sex = request.form['Sex']
    birth_date = request.form['Birth Date']
    primary_skills = request.form['Primary Skills']
    secondary_skill = request.form['Secondary Skill']
    company = request.form['Company']
    active = request.form['Active']
    country = request.form['Country']
    language = request.form['Language']

    search_token = [firstName, lastName, sex, birth_date, primary_skills,
                    secondary_skill, company, active, country, language]
    filtered = filterbyvalue(data, search_token)

    for i in filtered:
        i['times_seen'] += 1

    return render_template('search.html', title='results', result=filtered, providers=data)


def filterbyvalue(providers, token):
    results = providers
    if token[0]:
        results = [
            provider for provider in results if provider['first_name'] == str(token[0])]
    if token[1]:
        results = [
            provider for provider in results if provider['last_name'] == str(token[1])]
    if token[2] and token[2] != 'any':
        results = [
            provider for provider in results if provider['sex'] == token[2]]
    if token[3]:
        results = [
            provider for provider in results if provider['birth_date'] == token[3]]
    if token[4]:
        results = [
            provider for provider in results if str(token[4]) in provider['primary_skills']]
    if token[5]:
        results = [
            provider for provider in results if str(token[5]) in provider['secondary_skill']]
    if token[6]:
        results = [
            provider for provider in results if provider['company'] == str(token[6])]
    if token[7]:
        if token[7] == '1':
            results = [
                provider for provider in results if provider['active'] == True]
        else:
            results = [
                provider for provider in results if provider['active'] == False]
    if token[8]:
        results = [
            provider for provider in results if provider['country'] == str(token[8])]
    if token[9]:
        results = [
            provider for provider in results if provider['language'] == str(token[9])]

    results = sorted(results, key=lambda d: d['rating'], reverse=True)
    results = sorted(results, key=lambda d: d['times_seen'])

    return results
