<p align="center">
<a href="https://chartmogul.com"><img width="200" src="https://chartmogul.com/assets/img/logo.png"></a>
</p>

<h3 align="center">Official ChartMogul API Python Client</h3>

<p align="center"><code>chartmogul-python</code> provides convenient Python bindings for <a href="https://dev.chartmogul.com">ChartMogul's API</a>.</p>
<p align="center">
  <a href="https://www.npmjs.com/package/chartmogul-python"><img src="https://badge.fury.io/js/chartmogul-python.svg" alt="npm Package" /></a>
  <a href="https://travis-ci.org/chartmogul/chartmogul-python"><img src="https://travis-ci.org/chartmogul/chartmogul-python.svg?branch=master" alt="Build Status"/></a>
</p>
<hr>

<p align="center">
<b><a href="#installation">Installation</a></b>
|
<b><a href="#configuration">Configuration</a></b>
|
<b><a href="#usage">Usage</a></b>
|
<b><a href="#development">Development</a></b>
|
<b><a href="#contributing">Contributing</a></b>
|
<b><a href="#license">License</a></b>
</p>
<hr>
<br>

## Installation

This library requires Python 2.6 or 3 and above.

TODO - not on PyPI yet
TODO - separation of test/dev requirements
TODO - configuration for travis
TODO - set up tests for multiple python versions
TODO - icon for project release

```sh
pip install chartmogul
```

## Configuration

First create a `Config` object by passing your account token and secret key, available from the administration section of your ChartMogul account.

```python
import chartmogul
config = chartMogul.Config("token", "secret")
```

You need to pass this configuration object as the first argument to each request.

## Usage

The library is based on [promises](https://pypi.python.org/pypi/promise).
You can use it synchronously with `.get()`.

Here is an example:

```python
import chartmogul
config = chartMogul.Config("token", "secret")

req = chartmogul.Plan.create(config, data={...})
# Now either (asynchronous)
req.then(doSomething).catch(reactOnException)
# or (synchronous)
try:
    doSomething(req.get())
except Exception as ex:
    reactOnException(ex)
```

### Import API

Available methods in Import API:

#### [Data Sources](https://dev.chartmogul.com/docs/data-sources)

```python
chartmogul.DataSource.create(config)
chartmogul.DataSource.retrieve(config, uuid="data_source_uuid")
chartmogul.DataSource.all(config)
chartmogul.DataSource.destroy(config, uuid="data_source_uuid")
```

#### [Customers](https://dev.chartmogul.com/docs/customers)

```python
chartmogul.Customer.create(config, data={})
chartmogul.Customer.all(config, {
  page: 2,
  per_page: 20
})
chartmogul.Customer.destroy(config, uuid=customerUuid)
```

#### [Plans](https://dev.chartmogul.com/docs/plans)

```python
chartmogul.Plan.create(config, data={})
chartmogul.Plan.retrieve(config, uuid="")
chartmogul.Plan.modify(config, uuid="", data={
    "name": "new name"
})
chartmogul.Plan.all(config, page=2, external_id="")
chartmogul.Plan.destroy(config, uuid="")
```

#### [Invoices](https://dev.chartmogul.com/docs/invoices)

```python
ChartMogul.Import.Invoice.create(config, customerUuid, data)
ChartMogul.Import.Invoice.all(config, customerUuid, query)
```

#### [Transactions](https://dev.chartmogul.com/docs/transactions)

```python
ChartMogul.Import.Transaction.create(config, invoiceUuid, data)
```

#### [Subscriptions](https://dev.chartmogul.com/docs/subscriptions)

```python
ChartMogul.Import.Subscription.all(config, customerUuid, query)
ChartMogul.Import.Subscription.cancel(config, subscriptionUuid, {cancelled_at: ""})
ChartMogul.Import.Subscription.modify(config, subscriptionUuid, {cancellation_dates: []})
```

### Enrichment API

Available methods in Enrichment API:


#### [Customers](https://dev.chartmogul.com/docs/retrieve-customer)

```python
ChartMogul.Enrichment.Customer.retrieve(config, customerUuid)
ChartMogul.Enrichment.Customer.all(config, query)
ChartMogul.Enrichment.Customer.search(config, {
  email: 'adam@smith.com'
})

ChartMogul.Enrichment.Customer.merge(config, {
  "from": {"customer_uuid": "cus_5915ee5a-babd-406b-b8ce-d207133fb4cb"},
  "into": {"customer_uuid": "cus_2123290f-09c8-4628-a205-db5596bd58f7"}
})

ChartMogul.Enrichment.Customer.modify(config, "cus_5915ee5a-babd-406b-b8ce-d207133fb4cb", {
  "lead_created_at": "2015-01-01 00:00:00",
  "free_trial_started_at": "2015-06-13 15:45:13"
})
```

#### [Customer Attributes](https://dev.chartmogul.com/docs/customer-attributes)

```python
ChartMogul.Enrichment.Customer.attributes(config, customerUuid)
```

#### [Tags](https://dev.chartmogul.com/docs/tags)

```python
ChartMogul.Enrichment.Tag.add(config, customerUuid, {
  "tags": ["important", "Prio1"]
});
ChartMogul.Enrichment.Tag.add(config, {
  "email": 'adam@smith.com',
  "tags": ["important", "Prio1"]
});
ChartMogul.Enrichment.Tag.remove(config, customerUuid, {
  "tags": ["Prio1", "discountable"]
});
```


#### [Custom Attributes](https://dev.chartmogul.com/docs/custom-attributes)

```python
ChartMogul.Enrichment.CustomAttribute.add(config, customerUuid, {
  'custom': [
    {'type': 'Integer', 'key': 'age', 'value': 8}
  ]
});
ChartMogul.Enrichment.CustomAttribute.add(config, {
  'email': 'adam@smith.com',
  'custom': [
    {'type': 'Integer', 'key': 'age', 'value': 8}
  ]
});
ChartMogul.Enrichment.CustomAttribute.update(config, customerUuid, {
  'custom': {
    'age': 20,
    'channel': 'Twitter'
  }
});
ChartMogul.Enrichment.CustomAttribute.remove(config, customerUuid, {
  'custom': ['CAC']
});
```


### [Metrics API](https://dev.chartmogul.com/docs/introduction-metrics-api)

Available methods in Metrics API:


```python
ChartMogul.Metrics.all(config, {
  'start-date': '2015-01-01',
  'end-date': '2015-11-24',
  'interval': 'month',
  'geo': 'GB',
  'plans': 'Bronze Plan'
})
ChartMogul.Metrics.mrr(config, query)
ChartMogul.Metrics.arr(config, query)
ChartMogul.Metrics.arpa(config, query)
ChartMogul.Metrics.asp(config, query)
ChartMogul.Metrics.customerCount(config, query)
ChartMogul.Metrics.customerChurnRate(config, query)
ChartMogul.Metrics.mrrChurnRate(config, query)
ChartMogul.Metrics.ltv(config, query)
ChartMogul.Metrics.Customer.activities(config, customerUuid)
ChartMogul.Metrics.Customer.subscriptions(config, customerUuid)
```


### Errors

The library throws following error objects.

- `ChartMogul.ChartMogulError`
- `ChartMogul.ConfigurationError`
- `ChartMogul.ForbiddenError`
- `ChartMogul.NotFoundError`
- `ChartMogul.ResourceInvalidError`
- `ChartMogul.SchemaInvalidError`

The following table describes the properties of the error object.

|  Property  |       Type       |                             Description                             |
|:----------:|:----------------:|:-------------------------------------------------------------------:|
| `message`  | string           | The error message                                                   |
| `httpStatus`     | number           | When the error occurs during an HTTP request, the HTTP status code. |
| `response` | object or string | HTTP response as JSON, or raw response if not parsable to JSON |

## Development

To work on the library:

* Fork it
* Create your feature branch (`git checkout -b my-new-feature`)
* Install dependencies: TODO
* Fix bugs or add features. Make sure the changes pass the coding guidelines. TODO python lint
* Write tests for your new features. For HTTP mocking TODO library is used. Run tests with TODO and check test coverage with TODO
* If all tests are passed, push to the branch (`git push origin my-new-feature`)
* Create a new Pull Request

For a testing project we recommend setting up a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
with [development mode](https://packaging.python.org/installing/#installing-from-a-local-src-tree) installation
and [Jupyter](http://jupyter.org/).

Built using [Requests](https://github.com/kennethreitz/requests).

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/chartmogul/chartmogul-python.

## License

The library is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).

### The MIT License (MIT)

*Copyright (c) 2016 ChartMogul Ltd.*

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
