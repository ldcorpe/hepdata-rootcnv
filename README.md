# installation 
e.g on lxplus machine:
```
cd myWorkingDir 
virtualenv venv
source virtualenv/bin/activate
export PYTHONPATH=$PWD/lib/python2.7/site-packages
export PYTHONPATH=$PWD/local/lib64/python2.7/site-packages:$PYTHONPATH
export PATH="$PWD/bin:$PATH"
pip install -e . --prefix $PWD
```
# hepdata-rootcnv

Flexible ROOT conversion. Example:
```
./bin/hepdata-rootcnv example.yaml 
```

# write your own formatter
Some examples are given in `example.yaml`, but may not suit the structure of your data exactly.
You can write your own formatter to suit your needs. See `hepdatarootcnv/formatters.py` for some examples, and add yours there. 
