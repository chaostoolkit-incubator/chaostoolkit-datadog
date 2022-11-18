# Chaos Toolkit Extension Template

[![Version](https://img.shields.io/pypi/v/chaostoolkit-datadog.svg)](https://img.shields.io/pypi/v/chaostoolkit-datadog.svg)
[![License](https://img.shields.io/pypi/l/chaostoolkit-datadog.svg)](https://img.shields.io/pypi/l/chaostoolkit-datadog.svg)

![Build](https://github.com/chaostoolkit-incubator/chaostoolkit-datadog/workflows/Build/badge.svg)
[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-datadog.svg)](https://www.python.org/)

This project contains Chaos Toolkit activities and tolerances to work
with DataDog.

## Install

This package requires Python 3.7+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

[chaostoolkit]: https://github.com/chaostoolkit/chaostoolkit

```
$ pip install chaostoolkit-datadog
```

## Usage

A typical experiment using this extension would look like this:

```json
{
    "version": "1.0.0",
    "title": "Run a, experiment using a DataDog SLO to verify our system",
    "description": "n/a",
    "configuration": {
        "datadog_host": "https://datadoghq.eu"
    },
    "steady-state-hypothesis": {
        "title": "n/a",
        "probes": [
            {
                "type": "probe",
                "name": "read-slo",
                "tolerance": {
                    "type": "probe",
                    "name": "check-slo",
                    "provider": {
                        "type": "python",
                        "module": "chaosdatadog.slo.tolerances",
                        "func": "slo_must_be_met",
                        "arguments": {
                            "threshold": "7d"
                        }
                    }
                },
                "provider": {
                    "type": "python",
                    "module": "chaosdatadog.slo.probes",
                    "func": "get_slo",
                    "arguments": {
                        "slo_id": "..."
                    }
                }
            }
        ]
    },
    "method": []
}
```

That's it!

Please explore the code to see existing probes and actions.

## Configuration

In the `configuration` block you may want to specify the DataDog host you are
targetting:

```json
    "configuration": {
        "datadog_host": "https://datadoghq.eu"
    },
```

The authentication can be set using the typical DataDog environment variables,
notably:

* `DD_API_KEY`: the API key
* `DD_APP_KEY`: the application key

## Test

To run the tests for the project execute the following:

```
$ pytest
```

### Formatting and Linting

We use a combination of [`black`][black], [`flake8`][flake8], and [`isort`][isort]
to both lint and format this repositories code.

[black]: https://github.com/psf/black
[flake8]: https://github.com/PyCQA/flake8
[isort]: https://github.com/PyCQA/isort

Before raising a Pull Request, we recommend you run formatting against your
code with:

```console
$ make format
```

This will automatically format any code that doesn't adhere to the formatting
standards.

As some things are not picked up by the formatting, we also recommend you run:

```console
$ make lint
```

To ensure that any unused import statements/strings that are too long, etc.
are also picked up.

## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/
