import hashlib
from urllib import request
from xml.etree.ElementTree import canonicalize
import requests
from model import db
import json
import crud
from Crypto.Hash import SHA256
import datetime
from datetime import date
import os
import hmac
from hashlib import sha256
from Crypto.PublicKey import RSA 
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512 
import base64
from base64 import b64decode, b64encode 
from sqlalchemy import create_engine,Table, MetaData

# https://pypi.org/project/pycrypto/
engine = create_engine(os.environ["POSTGRES_URI"])
metadata = MetaData(engine)
class ProductFeed: 
    def __init__(self):
        print("init")
    def epoch_milliseconds(self,dt):
        "Walmart API accepts timestamps as epoch time in milliseconds"
        epoch = datetime.datetime.utcfromtimestamp(0)
        diff = dt-epoch
        return (diff.total_seconds() * 1000.0)

    def conocalize(self, headers):
        """Create signature map for hashing"""
        keys = headers.keys()
        sorted_keys = sorted(keys)

        canonicalize_string = ""
        parameter_names = ""
        for key in sorted_keys: 
            value = headers[key]
            parameter_names += key.strip() + ';'
            canonicalize_string += str(value).strip() + '\n'
        return [parameter_names, canonicalize_string]

    def generate_auth_signature(self, headers): 
        """Create auth signature"""

        array = self.conocalize(headers)

        secret = RSA.import_key(os.environ['PRIVATE_KEY'])
        # header_encoded= json.dumps(headers, sort_keys=True).encode()
        
        hash_val = SHA256.new(array[1].encode())
        signer = PKCS1_v1_5.new(secret)
        signature = signer.sign(hash_val)
        # hash_val = hmac.new(secret, msg=header_encoded, digestmod=hashlib.sha256).hexdigest()

        # int.from_bytes(sha256(secret+header_encoded).digest(), byteorder="big")
        # sig = base64.b64decode(hash_val+ '=' * (-len(hash_val) % 4))
        # 
        # print(sig)
        
        return str(b64encode(signature), 'utf-8')

    def walmart_auth_headers(self): 
        """Retrieve Time Stamp and Auth Signature"""
        
        headers = {
            'WM_SEC.KEY_VERSION': os.environ["WM_SEC_KEY_VERSION"],
            'WM_CONSUMER.ID': os.environ["WM_CONSUMER_ID"],
            'WM_CONSUMER.INTIMESTAMP':str(int(self.epoch_milliseconds(datetime.datetime.utcnow())))
        } 
        headers['WM_SEC.AUTH_SIGNATURE']=self.generate_auth_signature(headers)
        # headers['WM_CONSUMER.INTIMESTAMP']=)
        
        return headers
   
    def fetch(self, query, user_id):
        """ Get product for advice""" 
        # advice = crud.get_advice_by_id(feed)
        # url for trends: 
        # url = f'https://developer.api.walmart.com/api-proxy/service/affil/product/v2/trends'
        url= f'https://developer.api.walmart.com/api-proxy/service/affil/product/v2/search?query={query}&numItems=25'
        headers= self.walmart_auth_headers()


        walmart_products = requests.get(url, headers=headers)
        res = json.loads(walmart_products.text)

        if res.items():

            product_list=[[key,value] for key,value in res.items()]

            for product in product_list[6][1]:
                if product.get('name') and product.get('name') not in crud.get_advice():
                    # new_product_advice = crud.create_advice_for_user(product.get('name'), product.get('salePrice'), product.get('shortDescription'), product.get('itemId'), 3, product.get('largeImage'), user_id)
                    new_advice = Table("advice", metadata, autoload=True)
                    engine.execute(new_advice.insert(),advice_name=product.get('name'), advice_price=product.get('salePrice'), advice_description=product.get('shortDescription'), category_id=3, advice_info_id=product.get('itemId'), advice_img=product.get('largeImage'), user_id=user_id)
                    # db.session.add(new_product_advice)
                    # db.session.commit()
    
        return res

    def generate(self, query): 
        """Seed database with new queries"""
        # url for trends: 
        # url = f'https://developer.api.walmart.com/api-proxy/service/affil/product/v2/trends'
        url= f'https://developer.api.walmart.com/api-proxy/service/affil/product/v2/search?query={query}&numItems=25'
        headers= self.walmart_auth_headers()


        walmart_products = requests.get(url, headers=headers)
        res = json.loads(walmart_products.text)

        if res.items():

            product_list=[[key,value] for key,value in res.items()]

            for product in product_list[6][1]:
                if product.get('name') and product.get('name') not in crud.get_advice():
                    new_advice = Table("advice", metadata, autoload=True)
                    engine.execute(new_advice.insert(),advice_name=product.get('name'), advice_price=product.get('salePrice'), advice_description=product.get('shortDescription'), category_id=3, advice_info_id=product.get('itemId'), advice_img=product.get('largeImage'))
                    # new_product_advice = crud.create_advice(product.get('name'), product.get('salePrice'), product.get('shortDescription'), product.get('itemId'), 3, product.get('largeImage'))
                    # db.session.add(new_product_advice)
                    # db.session.commit()
    
        return res