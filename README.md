# document-converter
document-converter converts binary document file to markdown file by Azure Document Intelligence

## Before Use
### Install packages
This Repository use following packages.
* python-dotenv
* azure-ai-documentintelligence
* injector

So you should install packages.

Open a terminal window in your local environment and install library for Python with [pip](https://pypi.org/project/pip/):

```
$ pip install -r requirements.txt
```

### Edit `.env` file
You should edit `.env` file.

Open `.env` file and edit `DI_KEY` and `DI_ENDPOINT` value.
```
DI_KEY='abcdefghifklmn'
kI_ENDPOINT='https://xxxxxxxxxxxx.azure.com/'
```

## Usage
1. if not exists `source` and `output` folder, create on same directry as `main.py`.
1. Put your binary files to `source` folder. 
2. Open a terminal window and exec
```
python main.py
```
3. Check output files in `output` folder.
