from flask import Flask, redirect, url_for, request
from flask.templating import render_template
from numpy import random
import pandas as pd
import joblib

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/predict_calc')
def predict():
    model = joblib.load('Model rumah.sav')
    luast = int(request.args.get('x1'))
    luas = int(request.args.get('x2'))
    kamar = int(request.args.get('x3'))
    kamarm = int(request.args.get('x4'))
    lantai = int(request.args.get('x5'))
    garasi = int(request.args.get('x6'))
    dict = {'Luas Tanah': [luast],
            'Luas Bangunan': [luas],
            'Kamar': [kamar],
            'Kamar Mandi': [kamarm],
            'Jumlah Lantai': [lantai],
            'Garasi': [garasi]}
    payload = pd.DataFrame(dict)
    result = model.predict(payload)
    lower = str(int(result[0]*(90/100))) + '.00'
    lower = to_rupiah(lower)
    upper = str(int(result[0]*(110/100))) + '.00'
    upper = to_rupiah(upper)
    prediksi_dump = cut_num(lower) + ' - ' + cut_num(upper)
    return render_template('predict_calc.html', prediksi_dump = prediksi_dump, harga_recom = result[0])

@app.route('/kpr_calc_flat')
def kpr_calc_flat():
    #Cicilan bunga KPR dengan bunga flat
    #Bunganya tidak bertambah setiap tahunnya
    pred = int(request.args.get('kpr1'))
    suku = float(request.args.get('kpr2'))
    tahun = int(request.args.get('kpr3'))
    tenor = tahun*12
    cicilan_pokok = pred/tenor
    bunga = suku/1200

    minimal_bunga = bunga * pred
    cibul = cicilan_pokok + minimal_bunga

    total_bayar= cibul * tenor

    kpr_dump1 = to_rupiah(cibul)
    kpr_dump2 = to_rupiah(total_bayar)
    return render_template('kpr_calc.html', kpr_dump1 = kpr_dump1, kpr_dump2 = kpr_dump2)

@app.route('/kpr_calc_float')
def kpr_calc_float():
    type = request.args.get('type')
    print('INI', type)
    if type == 'efektif':
        # KPR float efektif
        total_pinjaman = int(request.args.get('kpr1'))
        tenor = int(request.args.get('kpr3'))
        suku_bunga = request.args.get('kpr2')
        suku_bunga = suku_bunga.split(',')
        ganti_suku = request.args.get('kpr4')
        ganti_suku = ganti_suku.split(',')

        dict_kpr = {
        'Tahun': [],
        'Bulan': [],
        'Bunga': [],
        'Angsuran Pokok': [],
        'Angsuran Bunga': [],
        'Total Angsuran': [],
        'Saldo Pinjaman': []
        }

        tahun = 0
        bulan = 0
        suku_iter = int(suku_bunga[0])
        angsuran_pokok = total_pinjaman / (tenor*12)

        for i in range((tenor*12)+1):
            if tahun == 0:
                dict_kpr['Tahun'].append(0)
                dict_kpr['Bulan'].append(0)
                dict_kpr['Bunga'].append('-')
                dict_kpr['Angsuran Pokok'].append('-')
                dict_kpr['Angsuran Bunga'].append('-')
                dict_kpr['Total Angsuran'].append('-')
                dict_kpr['Saldo Pinjaman'].append(total_pinjaman)

                tahun += 1
                bulan += 1
            else:
                dict_kpr['Tahun'].append(tahun)
                dict_kpr['Bulan'].append(bulan)

                for year_change in ganti_suku:
                    if tahun == int(year_change):
                        suku_iter = int(suku_bunga[ganti_suku.index(year_change) + 1])
                    
                angsuran_bunga = (dict_kpr['Saldo Pinjaman'][i-1] * (suku_iter/100) * tenor) / (tenor*12)
                dict_kpr['Bunga'].append(str(suku_iter) + '%')
                dict_kpr['Angsuran Pokok'].append(angsuran_pokok)
                dict_kpr['Angsuran Bunga'].append(angsuran_bunga)
                dict_kpr['Total Angsuran'].append(angsuran_pokok + angsuran_bunga)
                dict_kpr['Saldo Pinjaman'].append(dict_kpr['Saldo Pinjaman'][i-1] - angsuran_pokok)
                
                bulan += 1

                if bulan % 12 == 1:
                    tahun += 1
                    bulan = 1

        # kpr_dump1 = to_rupiah(cibul)
        # kpr_dump2 = to_rupiah(total_bayar)
        df_out = pd.DataFrame(dict_kpr)
        df_out = df_out.to_html(classes='table table-bordered table-striped table-dark')
        return render_template('kpr_df.html', result_df = df_out)
    else:
        # KPR float anuitas
        total_pinjaman = int(request.args.get('kpr1'))
        tenor = int(request.args.get('kpr3'))
        suku_bunga = request.args.get('kpr2')
        suku_bunga = suku_bunga.split(',')
        ganti_suku = request.args.get('kpr4')
        ganti_suku = ganti_suku.split(',')

        dict_kpr = {
        'Tahun': [],
        'Bulan': [],
        'Bunga': [],
        'Angsuran Pokok': [],
        'Angsuran Bunga': [],
        'Total Angsuran': [],
        'Saldo Pinjaman': []
        }

        tahun = 0
        bulan = 0
        suku_iter = int(suku_bunga[0])
        saldo_tahun = total_pinjaman

        for i in range((tenor*12)+1):
            if tahun == 0:
                dict_kpr['Tahun'].append(0)
                dict_kpr['Bulan'].append(0)
                dict_kpr['Bunga'].append('-')
                dict_kpr['Angsuran Pokok'].append('-')
                dict_kpr['Angsuran Bunga'].append('-')
                dict_kpr['Total Angsuran'].append('-')
                dict_kpr['Saldo Pinjaman'].append(total_pinjaman)

                tahun += 1
                bulan += 1
            else:
                dict_kpr['Tahun'].append(tahun)
                dict_kpr['Bulan'].append(bulan)

                for year_change in ganti_suku:
                    if tahun == int(year_change):
                        suku_iter = int(suku_bunga[ganti_suku.index(year_change) + 1])
                
                total_angsuran = saldo_tahun * ((suku_iter/100)/12) / (1-(1/(1+((suku_iter/100)/12))**(tenor*12)))
                angsuran_bunga = (dict_kpr['Saldo Pinjaman'][i-1] * (suku_iter/100) * tenor) / (tenor*12)
                angsuran_pokok = total_angsuran - angsuran_bunga
                dict_kpr['Bunga'].append(str(suku_iter) + '%')
                dict_kpr['Angsuran Pokok'].append(angsuran_pokok)
                dict_kpr['Angsuran Bunga'].append(angsuran_bunga)
                dict_kpr['Total Angsuran'].append(total_angsuran)
                dict_kpr['Saldo Pinjaman'].append(dict_kpr['Saldo Pinjaman'][i-1] - angsuran_pokok)
                
                bulan += 1

                if bulan % 12 == 1:
                    saldo_tahun = dict_kpr['Saldo Pinjaman'][i]
                    tahun += 1
                    bulan = 1

        # kpr_dump1 = to_rupiah(cibul)
        # kpr_dump2 = to_rupiah(total_bayar)
        df_out = pd.DataFrame(dict_kpr)
        df_out = df_out.to_html(classes='table table-bordered table-striped table-dark')
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
