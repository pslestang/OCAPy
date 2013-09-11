OCAPy
=====

OVH Client Api (in Python)

OCAPy is a python client implementing [OVH restful API](https://api.ovh.com/console/) consumption

## Disclaimer ##
**OVH is in no way involved in the development of this library**, in case of bug please use the issues tracker provided by Github

## Usage overview

```python
# Import the main class
>>> from OCAPy import OCAPy
>>> ocapy = OCAPy(profile='default')


>>> # And play with the API
... # A GET request: GET https://api.ovh.com/1.0/me
... request = ocapy.me.get()
>>> print request['city']
PLEUMELEUC


>>> # A GET request with parameters; GET https://api.ovh.com/1.0/ips?type=dedicated
... print ocapy.ip.get(params={'type': 'dedicated'})
[u'xx.xxx.xx.xxx/32', u'yy.yy.yyy.yyy/32']


>>> # Want to get a specific ressource?
... # GET https://api.ovh.com/1.0/ip/xx.xxx.xx.xxx%2F32
... print ocapy.ip('xx.xxx.xx.xxx/32').get()
{u'ip': u'xx.xxx.xx.xxx/32', u'type': u'dedicated'}


>>> # OK but I also want to play with POST and PUT!
... # POST https://api.ovh.com/1.0/me/ovhAccount/FR/creditOrder
... print ocapy.me.ovhAccount('FR').creditOrder.post(data={'amount':'1000'})
{u'totalWithTaxes': 10, u'currency': u'EUR', u'link': u'https://www.ovh.com/cgi-bin/order/displayOrder.cgi?orderId=12345678&orderPassword=Pl0p', u'expirationDate': u'2013-09-25T23:
29:59+02:00', u'totalWithoutTaxes': 10, u'password': u'Pl0p', u'id': 12345678}


>>> # PUT https://api.ovh.com/1.0/xdsl/xdsl-xxxx-1
... print ocapy.xdsl('xdsl-xxxx-1').put(data={'description':'My XDSL description'})
None


>>> # And what's about DELETE?
... # DELETE https://api.ovh.com/1.0/sms/sms-xxxx-1/user/ocapy
... print ocapy.sms('sms-xxxx-1').user('ocapy').delete()

None
>>>
```

### Basics
1. OVH API is available [here](https://api.ovh.com/console/)
2. To get your credentials follow [this tutorial](http://www.ovh.com/fr/g934.premiers-pas-avec-l-api)
3. The code has been tested with python 2.7

### Requirements
* The famous [requests > 1.0.0](http://docs.python-requests.org/en/latest/) python library
* To get color in ocapy program install [colorama](https://pypi.python.org/pypi/colorama) python library, **this requirement is NOT mandatory**
* Other libs should be available within your python installation.

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

### API Responses
- The API responses are **decoded JSON string**
- In case of **NULL** response, **None** is returned
- In case of **HTTP error** which is also an API error, an exception is raised

```python
>>> from OCAPy import OCAPy
>>> ocapy=OCAPy(profile='default')
>>> me=ocapy.me.get()
>>> # Ex: Adding ocapy user return a NULL response so None in python
... print ocapy.sms('sms-xxxx-1').users.post(data={'login':'ocapy', 'password':'plopplop'})
None
>>>
```

```python
>>> # Ex: Adding ocapy user one more time raise an exception:"
... try:
...     print ocapy.sms('sms-xxxx-1').users.post(data={'login':'ocapy', 'password':'plopplop'})
... except Exception as e:
...     print "Exception raise: %s" %e
...
Exception raise: POST https://api.ovh.com/1.0/sms/sms-xxxx-1/users [409]: This login exists already for that account
>>>
```

```python
>>> # Ex: Deleting ocapy user return a NULL response, so None in python
>>> print ocapy.sms('sms-xxxx-1').users('ocapy').delete()
None
>>>
```

```python
>>> # Calling an invalid resource, raise an exception:"
... try:
...     ocapy.me.invalidresource.get()
... except Exception as e:
...     print "Exception raised %s" % e
...
Exception raised GET https://api.ovh.com/1.0/me/invalidresource [404]: Got an invalid (or empty) URL
>>>
```

### Configuration
Starting from version **0.2.0** OCAPy is able to read authentication parameters from an INI configuration file. This configuration file is stored in the user's home directory and called **.ocapyrc**
The configuration is compounded of a main configuration part and one or several profiles part.

**Full exemple:**

```ini
[ocapy]
base_url = https://api.ovh.com/1.0/
profile = full

[profile-full]
name = full
app_key = 1234AbCD5eFGh6ijk
app_secret = QQkc0c1hqVnRWbmcwY3JtdDFDeFlkYkd
consumer_key = V2ROTnkwTzllMVJaZU9odDMxQzhxcGFk
base_url = https://api.ovh.com/1.0

[profile-domains]
name = domains
app_key = 1234AbCD5eFGh6ijk
app_secret = UemxsTVZKYVpVOW9kRE14UXpoeGNRmsK
consumer_key = UVlpLWVZwVk9XOWtSRTE0VVhwb2VHTlJ
base_url = https://api.ovh.com/1.0
```

To use the authentication parameters from the configuration file, just set the option ```profile='profile name'``` when instantiating the OCAPy class.
You may use the profile called 'default' to load the profile specified in ```[ocapy]``` section.

With the above configuration the following lines are strictly the same:

```python
# use the profile called full (profile-full)
ocapy = OCAPy(profile='full')
# use the default profile (value set to full) 
ocapy = OCAPy(profile='default')

```

### ocapy program
Starting from version **0.2.0** OCAPy is shipped with a program called ```ocapy``` which is for the moment a helper program that manages the configuration file (add, remove, detail, valid a profile)

The 'valid' utility tests that a request on https://api.ovh.com/1.0/me is working with a selected authentication profile 

During 'add' process the same request is done. If the test fails the profile is not added.

Here the help message:

```
usage: ocapy [-h] [-c] [-s] [-p PROFILE] [-n]

optional arguments:
  -h, --help            show this help message and exit
  -c, --config          Configure OCAPy and manage profiles authentication
  -s, --shell           Start an interactive shell
  -p PROFILE, --profile PROFILE
                        Authentication profile to use
  -n, --no-color        Disable color, default is to enable unless colorama
                        library is missing
```



### License
OCAPy is licensed under the terms of the General Public License v3
