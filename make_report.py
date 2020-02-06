import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import re
import io
import base64
import sys

survey_results_filename = sys.argv[1]

csv = pd.read_csv(survey_results_filename)
value_scores = {
    'Strongly agree': 2,
    'Agree': 1,
    'Neutral': 0,
    'Disagree': -1,
    'Strongly disagree': -2
}

general_re = re.compile(r'.+ \[(.+)\]')
extract_name = lambda col: general_re.search(col).group(1)
names = {extract_name(col) for col in csv.columns if general_re.match(col)}

def data_for_person(name):    
    p = re.compile(rf'(.+) \[{name}\]')
    cols = [col for col in csv.columns if p.match(col)]
    person_data = csv[cols]
    person_data.columns = [p.search(col).group(1) for col in person_data.columns]   
    person_data.replace(value_scores, inplace=True) 
    # dividing by len(names) because we dont have NA values.
    # In this poll, NA = Neutral = 0
    return person_data.sum().transpose() / len(names)

scores = pd.DataFrame([data_for_person(name) for name in names])
scores = scores.transpose()
scores.columns = names

def fig_to_base64(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png',
                bbox_inches='tight')
    img.seek(0)

    return base64.b64encode(img.getvalue())

def item_to_html(name, fig):
    fig_b64 = fig_to_base64(fig)
    fig_b64_utf8 = fig_b64.decode('utf-8')
    return f'''
    <p>
        {name}
        <br/>
        <img src="data:image/png;base64, {fig_b64_utf8}">
    </p>
'''

def report(name):
    items = []
    for question in scores.index:
        print(question)
        plt.figure(figsize=(10,1))
        ax = sns.swarmplot(scores.loc[question].transpose(), color='red')    
        ax.set_xlabel('')
        ax.set_xlim(-2,2)
        plt.axvline(x=scores[name][question], color='grey')
        # plt.show()
        items.append(item_to_html(question, plt))
    css = '''
p{
    font-size: 13px;
    font-family: 'Lato', sans-serif;
    margin-bottom: 30px;
}
img {
    width:100%;
}
''' 
    html = f'''
<html xmlns="https://www.w3.org/1999/xhtml"/>
<link href="https://fonts.googleapis.com/css?family=Lato&display=swap" rel="stylesheet">
<style>
{css}
</style>
{"".join(items)}
</html>
'''
    return html

for target_person in names:
    html = report(target_person)
    with open(f'{target_person}.report.html', 'wt') as out:
        out.write(html)

