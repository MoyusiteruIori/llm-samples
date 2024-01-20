# LLM Sample Codes

This repository contains example code for the winter break study sharing session during the 2024 graduation project at the School of Software Engineering, Tongji University.

If you want to run the code in this repository:

- Firstly, rename config.json.template to config.json and replace OPENAI_API_KEY with your own API key.

- It is recommended to use a separate Python execution environment. You can use conda, virtual environment, or any other tool. Here is an example of setting up a virtual environment:

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The above setup process has been tested only on Linux (Ubuntu) system. If you are using Windows or another platform, please make the necessary adjustments accordingly.

In addition, for countries or regions where accessing the OpenAI API is hindered due to well-known network issues, you may need to set up a network proxy or VPN on your own. The following code snippet is included in the sample code to address network issues:

```Python
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
```

If this interferes with the normal execution of other code for you, please remove it.