OCAPy
=====

OVH Client Api (in Python)

OCAPy is a python client implementing [OVH restful API](https://api.ovh.com/console/) consumption

## Disclaimer ##
**OVH is in no way involved in the development of this library**, in case of bug please use the issues tracker provided by Github

## Usage overview

```python
    # Import the main class
    from OCAPy import OCAPy
    
    # Instantiate OCAPy class
    ocapy=OCAPy(
        base_url='https://api.ovh.com/1.0/',
        app_key='YOUR APPLICATION KEY',
        app_secret='YOUR APPLICATION SECRET',
        consumer_key='YOUR CONSUMER KEY'
    )

    # And play with the API
    # A GET request: GET https://api.ovh.com/1.0/me
    request=ocapy.me.get()

    # print my city
    print request['city']

    # Want to get a specific ressource?
    # GET https://api.ovh.com/1.0/ip/213.186.33.99%2F32
    print ocapy.ip('213.186.33.99/32').get()
    
    # OK but I also want to play with POST and PUT!
    # POST https://api.ovh.com/1.0/me/ovhAccount/FR/creditOrder
    print ocapy.me.ovhAccount('FR').creditOrder.post(data={'amount':'1000'})

    # PUT https://api.ovh.com/1.0/xdsl/xdsl-xxxx-1
    print ocapy.xdsl('xdsl-xxxx-1').put(data={'description':'My XDSL description'})
    
    # And what's about DELETE?
    # DELETE https://api.ovh.com/1.0/sms/user/ocapy
    print ocapy.sms('sms-xxxx-1').user('ocapy').delete()
    
```

### Basics
1. OVH API is available [here](https://api.ovh.com/console/)
2. To get your credentials follow [this tutorial](http://www.ovh.com/fr/g934.premiers-pas-avec-l-api)
3. The code has been tested with python 2.7

### Requirements
* You only need the famous [requests > 1.0.0](http://docs.python-requests.org/en/latest/) python library
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

### Configuration
Starting from version **0.2.0** OCAPy is abble to read authentication parameters from an INI configuration file. This configuration file is stored in the user's home directory.
The configuration is compounded of a main configuration part and one or several profiles part. 

**Full exemple:**

```
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

To use the authentication parameters from the configuration file, just set the option ```ocapy_profile='profile name'``` when instantiating the OCAPy class.
You may use the profile called 'default' to load the profile specified in **```[ocapy]```** section.

With the above configuration the 2 following lines are strictly the same:

```python
from OCAPy import OCAPy

# use the profile called full (profile-full)
ocapy = OCAPy(ocapy_profile='full')
# use the default profile (value set to full) 
ocapy = OCAPy(ocapy_profile='default')

```

### ocapy program
Starting from version **0.2.0** OCAPy is shiped with a program called ```ocapy``` which is for the moment a helpfull program that manage configuration file.
When using it you are able to add, delete, detail an valid a profile authentication.

The 'valid' function tests that a request on https://api.ovh.com/1.0/me is working with an authentication profile 

During 'add' process, the same request is done, if the test fails, the profile is not added.

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

### API Responses
- The API responses are **decoded JSON string**
- In case of **NULL** response, **None** is returned
- In case of **HTTP error** which is also an API error, an exception is raised

```python
# A successfull request return a decoded JSON string
me=ocapy.me.get()
print "My name is: %s" % me['name']
```
    My name is: Le Stang

```python
# Ex: Adding ocapy user return a NULL response so None in python
print ocapy.sms('sms-xxxx-1').users.post(data={'login':'ocapy', 'password':'plopplop'})
```    
    None

```python    
# Ex: Adding ocapy user one more time raise an exception:"
try:
    ocapy.sms('sms-xxxx-1').users.post(data={'login':'ocapy', 'password':'plopplop'})
except Exception as e:
    print "Exception raised: %s" % e
```
    Exception raised: POST https://api.ovh.com/1.0/sms/sms-xxxx-1/users [409]: This login exists already for that account

```python
# Ex: Deleting ocapy user return a NULL response, so None in python"
print ocapy.sms('sms-xxxx-1').users('ocapy').delete()
```
    None

```python
# Calling an invalid resource, raise an exception:"
try:
    ocapy.me.invalidresource.get()
except Exception as e:
    print "Exception raised %s" % e

```
     Exception raised GET https://api.ovh.com/1.0/me/invalidresource [404]: Got an invalid (or empty) URL


### License
OCAPy is licensed under the terms of the General Public License v3
