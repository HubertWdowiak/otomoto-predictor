from bs4 import BeautifulSoup
import pandas as pd
import requests


def fetch_price(car_info):
    """fetch price from an offer page"""
    price = car_info.find('span', attrs={'class': 'offer-price__number'}).text
    try:
        price = ''.join(ch for ch in price if ch.isdigit())
        return {'price': int(price)}
    except:
        return {}


def fetch_date_and_id(car_info):
    """fetch and date and ID from an offer page"""
    date_and_id = car_info.findAll('span', attrs={'class': 'offer-meta__value'}, limit=2)
    id_int = int(''.join(ch for ch in date_and_id[1] if ch.isdigit()))
    return {'offer date': date_and_id[0].text, 'ID': id_int}


def fetch_params(car_info, columns=[]):
    """fetch basic offer params from an offer page"""
    offer_params = car_info.findAll('li', attrs={'class': 'offer-params__item'})
    params = {}
    try:
        for param in offer_params:
            label = param.find('span', attrs={'offer-params__label'}).text.strip()
            value = param.find(attrs={'offer-params__value'}).text.strip()
            params[label] = value
            columns.append(str(label))
        return params
    except:
        return params


def fetch_features(car_info, columns=[]):
    """fetch offer features"""
    offer_features = car_info.findAll('li', attrs={'class': 'offer-features__item'})
    features = {}
    try:
        for feature in offer_features:
            new_feature = feature.text.strip()
            features[new_feature] = True
            columns.append(str(new_feature))
        return features
    except:
        return features


def fetch_one_car(car_info, param_col=[], feature_col=[]):
    price = fetch_price(car_info)
    date_and_id = fetch_date_and_id(car_info)
    params = fetch_params(car_info, param_col)
    features = fetch_features(car_info, feature_col)
    return {**price, **date_and_id, **params, **features}


def fetch_one_page(otomoto_url, param_col=[], feature_col=[]):
    r = requests.get(otomoto_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    car_list = []

    for a in soup.findAll('a', attrs={'class': 'offer-title__link'}):
        car_content = requests.get(a['href'])
        car_info = BeautifulSoup(car_content.content, 'html.parser')
        cars = fetch_one_car(car_info, param_col, feature_col)
        car_list.append(cars)
    return car_list




def fetch_all_data(start_url, n_pages=100000, param_col=[], feature_col=[]):
    url = start_url
    car_list = []
    page = 0
    while page < n_pages:
        try:
            print(page)

            car_list += fetch_one_page(url, param_col, feature_col)
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            right_arrow = soup.find('a', attrs={'rel': 'next'})
            if right_arrow:
                url = right_arrow['href']
            else:
                print( f"nie ma szczałki strona={page}")
                break
            page += 1
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(e)
            page += 1

    return car_list


if __name__ == '__main__':

    import pandas as pd
    url = 'https://www.otomoto.pl/osobowe/uzywane/opel/?search%5Border%5D=created_at%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D=&l=1&page=40'
    params = []
    features = []
    car_list = fetch_all_data(url, param_col=params, feature_col=features)

    df = pd.DataFrame(car_list)
    df.to_csv('df10.csv')
    with open('params.txt', 'w') as file:
        for col in params:
            file.write(str(col)+',')
    with open('features.txt', 'w') as file:
        for col in features:
            file.write(str(col)+',')
