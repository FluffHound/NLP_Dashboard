from flask import Flask, redirect, url_for, request
from flask.templating import render_template
from numpy import random
import pandas as pd
import joblib

app = Flask(__name__)

@app.route('/welcome', methods=['GET', 'POST'])
def index():
    return render_template('welcome.html')

@app.route('/candidate')
def predict():

    return render_template('predict_calc.html')

@app.route('/kpr_calc_flat')
def kpr_calc_flat():
   
    return render_template('kpr_calc.html', kpr_dump1 = kpr_dump1, kpr_dump2 = kpr_dump2)

@app.route('/kpr_calc_float')
def kpr_calc_float():
        return render_template('kpr_df.html', result_df = df_out)

def to_rupiah(value):
    str_value = str(value)
    separate_decimal = str_value.split(".")
    after_decimal = separate_decimal[0]
    before_decimal = separate_decimal[1]

    reverse = after_decimal[::-1]
    temp_reverse_value = ""

    for index, val in enumerate(reverse):
        if (index + 1) % 3 == 0 and index + 1 != len(reverse):
            temp_reverse_value = temp_reverse_value + val + "."
        else:
            temp_reverse_value = temp_reverse_value + val

    temp_result = temp_reverse_value[::-1]

    return "Rp " + temp_result

def cut_num(angka):
    if len(angka) > 12:
        if angka[5] == '0':
            return str(angka[3] + ' M')
        else:
            return str(angka[3] + ',' + angka[5] + ' M')
    else:
        return str(angka + ' Juta')

@app.route('/preview')
def preview_house():
    daerah = request.args.get('daerah')
    dataset = pd.read_csv('Dataset rumah123 CLEAN.csv')
    dataset = dataset.drop('index', 1)
    frag_data = dataset.loc[dataset['Alamat'].isin([daerah])].reset_index().drop('index', 1)
    feature_preview = []
    img_preview = []
    link_preview = []

    for i in range(3):
        chooser = random.randint(len(frag_data))
        chosen = frag_data.loc[[chooser]]
        chosen_feature = [chosen['Kamar'].values.tolist(), chosen['Kamar Mandi'].values.tolist(), chosen['Garasi'].values.tolist()]
        chosen_img = chosen['IMG Link'].values.tolist()
        chosen_link = chosen['Link'].values.tolist()
        
        for feature in chosen_feature:
            for element in feature:
                feature_preview.append(element)
        for link in chosen_img:
            img_preview.append(link)
        for link in chosen_link:
            link_preview.append(link)
    
    return render_template('daerah_preview.html', feature_preview = feature_preview, img_preview = img_preview, alamat = daerah, link_preview = link_preview, daerah_pred = daerah)

@app.route('/kpr_select')
def kpr_select():
    kpr_type = request.args.get('kpr')
    if kpr_type == 'flat':
        return render_template('kpr_flat.html')
    else:
        return render_template('kpr_float.html', kpr_type = kpr_type)

@app.route('/recommendation')
def recommendation():
    daerah = request.args.get('daerah')
    harga_pred = float(request.args.get('harga_pred'))
    print(harga_pred, 'THIS')
    print(type(harga_pred))
    up_const = 110
    down_const = 90
    nye = harga_pred*(down_const/100)
    print(harga_pred)
    print(nye)
    dataset = pd.read_csv('Dataset rumah123 CLEAN.csv')
    dataset = dataset.drop('index', 1)
    frag_data = dataset.loc[dataset['Alamat'].isin([daerah])].reset_index().drop('index', 1)

    while True:
        final_data = frag_data[(frag_data['Harga'] > harga_pred*(down_const/100)) & (frag_data['Harga'] < harga_pred*(up_const/100))].reset_index().drop('index', 1)
        if len(final_data) < 4:
            up_const += 10
            down_const -= 10
            continue
        else:
            break
    
    feature_recom = []
    img_recom = []
    link_recom = []
    harga_recom = []

    for i in range(4):
        chooser = random.randint(len(final_data))
        chosen = final_data.loc[[chooser]]
        chosen_feature = [chosen['Kamar'].values.tolist(), chosen['Kamar Mandi'].values.tolist(), chosen['Garasi'].values.tolist()]
        chosen_img = chosen['IMG Link'].values.tolist()
        chosen_link = chosen['Link'].values.tolist()
        chosen_price = chosen['Harga'].values.tolist()
        
        for feature in chosen_feature:
            for element in feature:
                feature_recom.append(element)
        for link in chosen_img:
            img_recom.append(link)
        for link in chosen_link:
            link_recom.append(link)
        for price in chosen_price:
            price = str(int(price)) + '.00'
            price = cut_num(to_rupiah(price))
            harga_recom.append(price)

    return render_template('daerah_recom.html', feature_recom = feature_recom, img_recom = img_recom, link_recom = link_recom, harga_recom = harga_recom, alamat = daerah)

if __name__ == '__main__':
    app.run(debug = True)
