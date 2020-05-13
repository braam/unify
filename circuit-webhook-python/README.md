# circuit-webhook

[![PyPI](https://img.shields.io/pypi/v/circuit-webhook)](https://pypi.org/project/circuit-webhook/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/circuit-webhook)](https://pypi.org/project/circuit-webhook/)
[![Downloads](https://pepy.tech/badge/circuit-webhook)](https://pepy.tech/project/circuit-webhook)

circuit-webhook is a python client library for Unify Circuit api Incoming Webhooks on Python 3.6 and above.


## Installation

    $ pip install circuit-webhook

## Usage

```python
from circuit_webhook import Circuit

circuit = Circuit(url='https://eu.yourcircuit.com/rest/v2/webhooks/incoming/XXX')
circuit.post(text="Hello, world.")
```

## Getting started

For help getting started with Incoming Webhooks, view online [documentation](https://circuit.github.io/webhooks.html).


## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
