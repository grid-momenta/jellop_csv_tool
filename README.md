# Desktop App

## Running python app

Install python virtual env:

```shell
sudo pip install virtualenv
```

Browse to project folder.

Start virtual env and activate:

```shell
virtualenv venv
source venv/bin/activate
```

Install packages:

```shell
pip install -r requirements.txt
```

Run project:

```shell
flet run main.py -d
```

The UI will be appeared:

![img_2.png](img.png)

## Creating desktop app

```shell
flet pack main.py

flet pack main.py --product-name "Jellop CSV Tool" --product-version "0.0.1" --copyright "Copyright @ Jellop 2023" --bundle-id "com.jellop.csv_tool"
```

For more details check [flet.dev docs](https://flet.dev/docs/guides/python/packaging-desktop-app)