Python module for parsing json.

Requirments:
* PCRE 8.x
* python-pcre
* python 3.x

Installation dependencies:
    
Install PCRE libraries:

For Debian, Ubuntu and related Linux:
    
    sudo apt-get install libpcre3-dev
    
For CentOS:
    
    sudo apt-get install libpcre3-dev
    
For Mac:

    brew install pcre
    
For Mac without brew:
 
Go to https://www.pcre.org/ and download latest pcre.

    tar -xzvf pcre-8.42.tar.gz
    cd pcre-8.42
    ./configure --prefix=/usr/local/pcre-8.42
    make
    make install
    ln -s /usr/local/pcre-8.42 /usr/sbin/pcre
    ln -s /usr/local/pcre-8.42/include/pcre.h /usr/include/pcre.h

Install python-pcre module:
    
    pip install python-pcre

or 

    pip install -r requirements.txt
    
    
Example usage (in code):
    
    json = '{"kek": {"null": "kekich", "lol1": [1, 2]}, "kek1": [4, 5], "opa1": null, "opa2": "null"}'
    res_obj = JsonParser.loads(json)
    res_str = JsonParser.dumps(res_obj)
    
    print(res_obj, type(res_obj), '', res_str, type(res_str), sep='\n')
    
Example usage (from command line):

Script expects minimum 2 arguments (if you don't want get help).
    
Possible flags:
    
    -h|--help - for showing instructions
    -s|--str - to get json as string from arguments
    -f|--file - to read json string from file 
    -e|--encoding - to read from file in correct encoding (default: utf-8)
    -u|--url - to get json from url
    
Usage examples:

    python json_parser.py -h
    python json_parser.py -s 'json_string'
    python json_parser.py -f path_to_file [-e ASCII]
    python json_parser.py -u url_to_json
    

