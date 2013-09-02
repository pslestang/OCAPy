OCAPy
=====

OCAPy is a python client implementation to use with OVH restful API

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
    # A GET request
    request=ocapy.me.get()

    # print my city
    print request['city']

    # Want to get a specific ressource?
    print ocapy.ip('213.186.33.99/32').get()
    
    # OK but I also want to play with POST and PUT
    print ocapy.me.ovhAccount('FR').creditOrder.post(data={'amount':'1000'})
    print ocapy.xdsl('xdsl-xxxx-1').put(data={'description':'My XDSL description'})
    
    # And what about DELETE
    print ocapy.sms('sms-xxxx-1').user('ocapy').delete()
    
```

## Basics
1. OVH API is available [here](https://api.ovh.com/console/)

2. To get your credentials follow [this tutorial](http://www.ovh.com/fr/g934.premiers-pas-avec-l-api)

## Requirements
You need the [famous requests](http://docs.python-requests.org/en/latest/) python library

## License
OCAPy is licensed under GPLv3
