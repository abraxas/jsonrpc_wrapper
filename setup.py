from distutils.core import setup
setup(name='jsonrpc_wrapper',
      version='0.1',
      packages=["jsonrpc_wrapper"],
      author="Charles Martin",
      author_email="cjay.martin@gmail.com",
      url="https://github.com/abraxas/jsonrpc_wrapper",
      description="A simple library to create a json_rpc interface around classes *without* mandating protocol or controlling flow.",
      requires=["json"],
      )
