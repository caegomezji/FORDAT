# FORDAT
DS4A - T8 Project Repository

## Requeriments

- Docker 

## Installation

``` bash

# clone project
git clone https://github.com/caegomezji/FORDAT.git

# set the env variables
cp .env.example .env
# edit env
nano .env

```

## DEVELOPMENT DEPLOYMENT 

Edit the `.env` file and set the variable `APP_ENV` as `DEVELOPMENT`

``` bash

APP_ENV=DEVELOPMENT 

```


``` bash

# give permisions and init docker
chmod +x ./init.sh
./init.sh


```


## PRODUCTION DEPLOYMENT 

Edit the `.env` file and set the variable `APP_ENV` as `PRODUCTION`

``` bash

APP_ENV=PRODUCTION 

```


``` bash

# give permisions and init docker
chmod +x ./init.sh
./init.sh


```
