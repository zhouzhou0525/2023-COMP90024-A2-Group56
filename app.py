# Group56 Team members:

# Ziyi Wang (Student ID: 1166087)
# Zhou Zhou (Student ID: 1234764)
# Xiangyi He (Student ID: 1166146)
# Boyu Pan (Student ID: 1319288)
# Huating Ji (Student ID: 1078362)

# README: instructions on flasl
# 1. Install needed package:
# pip install flask
# pip install pandas
# pip install couchdb
# 2. Run flask
# python app.py

from flask import Flask, render_template, request, redirect, Response
import pandas as pd
from flask_cors import CORS
from flask import send_file
from flask import Flask, render_template, request
import couchdb



url = 'http://admin:15011010377@172.26.134.151:5984'
couch = couchdb.Server(url)
ms_url = 'http://admin:15011010377@172.26.134.50:5984'
ms_couch = couchdb.Server(ms_url)


cor={'1gsyd': 'Great Sydney', '2gmel': 'Great Melbourne',
     '3gbri': 'Great Brisbane', '4gade': 'Great Adelaide',
     '5gper': 'Great Perth', '6ghob': 'Great Hobart',
     '7gdar': 'Great Darwin', '8acte': 'Australian Capital \n Territory',
     '9oter': 'Other'
     }

rev_cor = {'Great Sydney':'1gsyd', 'Great Melbourne':'2gmel',
     'Great Brisbane': '3gbri', 'Great Adelaide': '4gade',
     'Great Perth': '5gper', 'Great Hobart': '6ghob',
     'Great Darwin': '7gdar' , 'Australian Capital \n Territory': '8acte',
     'Other': '9oter'
     }

month = {'2':'Feb', '3':'Mar', '4':'Apr', '5':'May',
         '6':'Jun', '7':'Jul', '8':'Aug'}

cities = {'Melbourne': '2gmel','Sydney': '1gsyd', 'Perth': '5gper',
          'Brisbane': '3gbri', 'Adelaide': '4gade', 'Darwin': '7gdar',
          'Hobart': '6ghob', 'Australian Capital Territory': '8acte'}


app = Flask(__name__)
CORS(app)



@app.route('/view2')
def view2():
    db = couch['view2_gcc_count']
    query = {
        "selector": {
            "$or": [
                {"_id": {
                    "$regex": "g"
                }
                },
                {"_id": {
                    "$regex": "8"
                }
                },
                {"_id": {
                    "$regex": "9"
                }
                }
            ]
        }
    }
    return_list = []
    for rows in db.find(query):
        if not rows == "None":
            dict = {}
            dict['value'] = rows['value']
            dict['name'] = cor[rows['_id']]
            return_list.append(dict)
    db1 = couch['view3_syd']
    db2 = couch['view3_mel']
    db3 = couch['view3_bri']
    r_list = [['']]
    for id in db1:
        if not id[2:7] in r_list[0]:
            r_list[0].append(id[2:7])
        r_list.append([id[11:-2]])
    i = 1
    for id in db1:
        r_list[i].append(db1[id]['value'])
        i = i + 1
    i = 1
    for id in db2:
        if not id[2:7] in r_list[0]:
            r_list[0].append(id[2:7])
        r_list[i].append(db2[id]['value'])
        i = i + 1
    i = 1
    for id in db3:
        if not id[2:7] in r_list[0]:
            r_list[0].append(id[2:7])
        r_list[i].append(db3[id]['value'])
        i = i + 1
    db4 = couch['view4_ball_event']
    r_list_4 = []
    for id in db4:
        if id[17:-2] != 'None':
            dict = {}
            dict['value'] = db4[id]['value']
            dict['name'] = id[17:-2]
            r_list_4.append(dict)

    return [return_list, r_list[:-1], r_list_4]


@app.route('/view5')
def view5():
    db = couch['view5_sentiment']
    name_list = []
    pros = []
    cons = []
    for id in db:
        if id[1:-13] != 'None':
            if not id[2:-14] in name_list:
                name_list.append(id[2:-14])
            if id[-10:-2] == 'positive':
                pros.append(db[id]['value'])
            elif id[-10:-2] == 'negative':
                cons.append(db[id]['value'])
    l1 = [name_list, pros, cons]
    db1 = ms_couch['vmas1_sport_type']
    db2 = ms_couch['vmas2_positive_sport_type']
    n_list = []
    t_list = []
    p_list = []
    for rows in db1:
        if db1[rows]['id'] != 'None':
            n_list.append(db1[rows]['id'])
            t_list.append(db1[rows]['value'])
    for rows in db2:
        if db2[rows]['id'] != 'None':
            p_list.append(db2[rows]['value'])
    c_list = []
    for i in range(len(t_list)):
        c_list.append(t_list[i]-p_list[i])
    l2 = [n_list, c_list, p_list]
    return [l1, l2]


@app.route('/view6')
def view6():
    db = couch['view6_vic_type']
    name_list = []
    gm_list = []
    vr_list = []
    for id in db:
        if id[-5:-1] != 'None':
            if id[2:6] != 'None':
                if not id[11:-2] in name_list:
                    name_list.append(id[11:-2])
                if id[2:7] == '2gmel':
                    gm_list.append(db[id]['value'])
                if id[2:7] == '2rvic':
                    vr_list.append(db[id]['value'])
    return [name_list, gm_list, vr_list]



@app.route('/view1')
def view1():
    db1 = couch['view1_month']
    db2 = couch['view1_month_event']
    db3 = couch['view1_month_type']
    l1 = []
    for id in db1:
        if id == '6':
            dict = {}
            dict['value'] = db1[id]['value']
            dict['itemSytle'] = {'color': '#a90000'}
            l1.append(dict)
        else:
            l1.append(db1[id]['value'])
    event_list = []
    node_list = [{'name': "Total"}]
    for id in db2:
        n_id = id[5:-2]
        if n_id != 'None':
            event_list.append({'value': db2[id]['value'],
                               'name': n_id})
            node_list.append({'name': n_id})
    type_list = []
    for id in db3:
        n_id = id[5:-2]
        if n_id != 'on':
            type_list.append({'value': db3[id]['value'],
                               'name': n_id})
            node_list.append({'name': n_id})
    link_list = []
    for item in type_list:
        dict = {
            "source": "Total", "target": item['name'],
            "value": item['value']
        }
        link_list.append(dict)
    for item2 in event_list:
        dict = {
            "source": "Ball Sports", "target": item2['name'],
            "value": item2['value']
        }
        link_list.append(dict)
    return [l1, node_list, link_list]



@app.route('/view4')
def view4():
    db = couch['view4_ball_event']
    r_list = []
    for id in db:
        if id[17:-2] != 'None':
            dict = {}
            dict['value'] = db[id]['value']
            dict['name'] = id[17:-2]
            r_list.append(dict)
    return r_list


@app.route('/view7')
def view7():
    list1 = view7_1()
    list2 = view7_2()
    return [list1, list2]


def view7_1():
    db = couch['view6_vic_type']
    name_list = []
    gm_list = []
    n_list = []
    for id in db:
        if id[-5:-1] != 'None':
            if id[2:6] != 'None':
                if not id[11:-2] in name_list:
                    name_list.append(id[11:-2])
                    dict = {}
                    dict['name'] = id[11:-2]
                    dict['max'] = 0.8
                    n_list.append(dict)
                if id[2:7] == '2gmel':
                    gm_list.append(db[id]['value'])
    v_list2 = []
    db2 = couch['view3_mel']
    for gen in name_list:
        for id in db2:
            if id[11:-2] == gen:
                v_list2.append(db2[id]['value'])
    pl1 = []
    pl2 = []
    for i in range(len(n_list)):
        pl1.append(gm_list[i] / sum(gm_list))
        pl2.append(v_list2[i] / sum(v_list2))
    return [n_list, pl1, pl2]


def view7_2():
    db = couch['view7_bri']
    n_list = []
    v_list = []
    genre_name = []
    for id in db:
        if id != 'None':
            v_list.append(db[id]['value'])
            dict = {}
            dict['name'] = id
            genre_name.append(id)
            dict['max'] =0.7
            n_list.append(dict)
    v_list2 = []
    db2 = couch['view3_bri']
    for gen in genre_name:
        for id in db2:
            if id[11:-2] == gen:
                v_list2.append(db2[id]['value'])
    pl1 = []
    pl2 = []
    for i in range(len(n_list)):
        pl1.append(v_list[i]/sum(v_list))
        pl2.append(v_list2[i]/sum(v_list2))
    return [n_list, pl1, pl2]


@app.route('/view3')
def view3():
    db1 = couch['view3_syd']
    db2 = couch['view3_mel']
    db3 = couch['view3_bri']
    r_list = [['']]
    for id in db1:
        if not id[2:7] in r_list[0]:
            r_list[0].append(id[2:7])
        r_list.append([id[11:-2]])
    i = 1
    for id in db1:
        r_list[i].append(db1[id]['value'])
        i = i+1
    i = 1
    for id in db2:
        if not id[2:7] in r_list[0]:
            r_list[0].append(id[2:7])
        r_list[i].append(db2[id]['value'])
        i = i+1
    i = 1
    for id in db3:
        if not id[2:7] in r_list[0]:
            r_list[0].append(id[2:7])
        r_list[i].append(db3[id]['value'])
        i = i+1
    return r_list[:-1]


@app.route('/events/by_month')
def genre_by_month():
    db1 = couch['view4_month_bri']
    db2 = couch['view4_month_mel']
    db3 = couch['view4_month_syd']
    r_list = [['Aug', []],
              ['Jul', []],
              ['Jun', []],
              ['May', []],
              ['Apr', []],
              ['Mar', []],
              ['Feb', []]]
    i = 6
    for id in db1:
        r_list[i][1].append(db1[id]['value'])
        i -= 1
    i = 6
    for id in db2:
        r_list[i][1].append(db2[id]['value'])
        i -= 1
    i = 6
    for id in db3:
        r_list[i][1].append(db3[id]['value'])
        i -= 1
    return r_list

@app.route('/view8')
def view8():
    db = couch['view2_gcc_count']
    query = {
        "selector": {
            "$or": [
                {"_id": {
                    "$regex": "g"
                }
                },
                {"_id": {
                    "$regex": "8"
                }
                },
                {"_id": {
                    "$regex": "9"
                }
                }
            ]
        }
    }
    n_list = []
    twi_list = []
    for rows in db.find(query):
        if rows != "None":
            if cor[rows['_id']] != "Other":
                twi_list.append(rows['value'])
                n_list.append(cor[rows['_id']])
    db2 = couch['life_dbs']
    dict = {}
    for id in db2:
        dict[cor[cities[id]]] = db2[id]['value']
    life_list = []
    name_list = []
    for name in n_list:
        life_list.append(dict[name])
        name_list.append(rev_cor[name])
    db3 = couch["income_annual_dbs"]
    query3 = {
        "selector": {
            "$or": [
                {"gccsa_code": {
                    "$regex": "g"
                }
                },
                {"gccsa_code": {
                    "$regex": "8"
                }
                }
            ]
        }
    }
    income_list = []
    for rows in db3.find(query3):
        if not rows == "None":
            income_list.append(int(rows['sum_aud_2017_18']))
    return [name_list, twi_list, life_list, income_list]


@app.route('/ms_view1')
def ms_view1():
    db1 = ms_couch['vmas1_sport_type']
    db2 = ms_couch['vmas2_positive_sport_type']
    n_list = []
    t_list = []
    p_list = []
    for rows in db1:
        if db1[rows]['id'] != 'None':
            n_list.append(db1[rows]['id'])
            t_list.append(db1[rows]['value'])
    for rows in db2:
        if db2[rows]['id'] != 'None':
            p_list.append(db2[rows]['value'])
    return [n_list, t_list, p_list]


@app.route('/ms_view2')
def ms_view2():
    db = ms_couch['vmas3_sport_event']
    r_list = []
    for rows in db:
        if db[rows]['id'] != 'None':
            dict = {}
            dict['value'] = db[rows]['value']
            dict['name'] = db[rows]['id']
            r_list.append(dict)
    return r_list


@app.route('/cob')
def cob():
    return send_file('templates/testmap.png', mimetype='image/gif')

if __name__ == "__main__":
    app.run(host='172.26.135.65', port=5000, debug=True)

