OCAPy
=====

OVH Client Api (in Python)

OCAPy is a python client implementing OVH restful API consumption

## Disclaimer ##
**OVH is IN NO WAY involved in the development of this library**, in case of bug please use the issues tool provided by Github

## Quick usage overview

```python
    # Instantiate OCAPy class
    ocapy=OCAPy(
        base_url='https://api.ovh.com/1.0/',
        app_key='YOUR APPLICATION KEY',
        app_secret='YOUR APPLICATION SECRET',
        consumer_key='YOUR CONSUMER KEY'
    )

    # And play with the API
    # A GET request: GET https://api.ovh.com/1.0/me/
    request=ocapy.me.get()

    # print my city
    print request['city']

    # Want to get a specific ressource?
    # GET https://api.ovh.com/1.0/ip/213.186.33.99%2F/
    print ocapy.ip('213.186.33.99/32').get()
    
    # OK but I also want to play with POST and PUT!
    # POST https://api.ovh.com/1.0/me/ovhAccount/FR/creditOrder/
    print ocapy.me.ovhAccount('FR').creditOrder.post(data={'amount':'1000'})

    # PUT https://api.ovh.com/1.0/xdsl/xdsl-xxxx-1/
    print ocapy.xdsl('xdsl-xxxx-1').put(data={'description':'My XDSL description'})
    
    # And what's about DELETE?
    # DELETE https://api.ovh.com/1.0/sms/user/ocapy/
    print ocapy.sms('sms-xxxx-1').user('ocapy').delete()
    
```

## What you need to know
### Basics
1. OVH API is available [here](https://api.ovh.com/console/)
2. To get your credentials follow [this tutorial](http://www.ovh.com/fr/g934.premiers-pas-avec-l-api)
3. The code has been tested with python 2.7

### Requirements
1. You only need the famous [requests](http://docs.python-requests.org/en/latest/) python library, other libs should be available with your python installation.

### Installation
1. Download the archive
2. Unzip and go into the directory
3. run ```python setup.py install```
4. Play with it!

In other words under Linux:

```bash
wget https://github.com/pslestang/OCAPy/archive/master.zip
unzip master.zip
cd OCAPy-master/
sudo python setup.py install
```

### License
OCAPy is licensed under GPLv3
