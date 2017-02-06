<p align='center'>
<a href='https://chartmogul.com'><img width='200' src='https://chartmogul.com/assets/img/logo.png'></a>
</p>

<h3 align='center'>Official ChartMogul API Python Client</h3>

<p align='center'><code>chartmogul-python</code> provides convenient Python bindings for <a href='https://dev.chartmogul.com'>ChartMogul's API</a>.</p>
<p align='center'>
  <a href="https://badge.fury.io/py/chartmogul"><img src="https://badge.fury.io/py/chartmogul.svg" alt="PyPI version" height="18"></a>
  <a href='https://travis-ci.org/chartmogul/chartmogul-python'><img src='https://travis-ci.org/chartmogul/chartmogul-python.svg?branch=master' alt='Build Status'/></a>
</p>
<hr>

<p align='center'>
<b><a href='#installation'>Installation</a></b>
|
<b><a href='#configuration'>Configuration</a></b>
|
<b><a href='#usage'>Usage</a></b>
|
<b><a href='#development'>Development</a></b>
|
<b><a href='#contributing'>Contributing</a></b>
|
<b><a href='#license'>License</a></b>
</p>
<hr>
<br>

## Installation

This library requires Python 2.6, 2.7 or 3.2 and above.

```sh
pip install chartmogul
```

## Configuration

First create a `Config` object by passing your account token and secret key, available from the administration section of your ChartMogul account.

```python
import chartmogul
config = chartMogul.Config('token', 'secret')
```

You need to pass this configuration object as the first argument to each request.

## Usage

The library is based on [promises](https://pypi.python.org/pypi/promise).
You can use it synchronously with `.get()`.

Here is an example:

```python
import chartmogul
config = chartMogul.Config('token', 'secret')

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
chartmogul.DataSource.retrieve(config, uuid='ds_5915ee5a-babd-406b-b8ce-d207133fb4cb')
chartmogul.DataSource.all(config)
chartmogul.DataSource.destroy(config, uuid='ds_5915ee5a-babd-406b-b8ce-d207133fb4cb')
```

#### [Customers](https://dev.chartmogul.com/docs/customers)

```python
chartmogul.Customer.create(config, data={})
chartmogul.Customer.all(config, {
  page: 2,
  per_page: 20
})
chartmogul.Customer.retrieve(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb')
chartmogul.Customer.search(config, email='email@email.com')
chartmogul.Customer.merge(config, data={
  'from': {'customer_uuid': 'cus_5915ee5a-babd-406b-b8ce-d207133fb4cb'},
  'into': {'customer_uuid': 'cus_2123290f-09c8-4628-a205-db5596bd58f7'}
})
chartmogul.Customer.modify(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb', data={
  'from': {'customer_uuid': 'cus_5915ee5a-babd-406b-b8ce-d207133fb4cb'},
  'into': {'customer_uuid': 'cus_2123290f-09c8-4628-a205-db5596bd58f7'}
})
chartmogul.Customer.destroy(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb')
```

#### [Customer Attributes](https://dev.chartmogul.com/docs/customer-attributes)

```python
chartmogul.Attributes.retrieve(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb')
```

#### [Tags](https://dev.chartmogul.com/docs/tags)

```python
chartmogul.Tags.add(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb', data={
  'tags': ['important', 'Prio1']
})
chartmogul.Tags.add(config, data={
  'email': 'adam@smith.com',
  'tags': ['important', 'Prio1']
})
chartmogul.Tags.remove(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb', data={
  'tags': ['important', 'Prio1']
})
```

#### [Custom Attributes](https://dev.chartmogul.com/docs/custom-attributes)

```python
chartmogul.CustomAttributes.add(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb', data={
  'custom': [
    {'type': 'Integer', 'key': 'age', 'value': 8}
  ]
})
chartmogul.CustomAttributes.add(config, data={
  'email': 'adam@smith.com',
  'custom': [
    {'type': 'Integer', 'key': 'age', 'value': 8}
  ]
})
chartmogul.CustomAttributes.update(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb', data={
  'custom': {
    'age': 20,
    'channel': 'Twitter'
  }
});
chartmogul.CustomAttributes.remove(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb', data={
  'custom': ['CAC']
})
```

#### [Plans](https://dev.chartmogul.com/docs/plans)

```python
chartmogul.Plan.create(config, data={})
chartmogul.Plan.retrieve(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb')
chartmogul.Plan.modify(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb', data={
    'name': 'new name'
})
chartmogul.Plan.all(config, page=2, external_id='')
chartmogul.Plan.destroy(config, uuid='')
```

#### [Invoices](https://dev.chartmogul.com/docs/invoices)

```python
chartmogul.Invoice.create(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb', data={})
chartmogul.Invoice.all(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb', page=2, per_page=10)
```

#### [Transactions](https://dev.chartmogul.com/docs/transactions)

```python
chartmogul.Transaction.create(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb', data={})
```

#### [Subscriptions](https://dev.chartmogul.com/docs/subscriptions)

```python
chartmogul.Subscription.all(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb')
chartmogul.Subscription.cancel(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb' data={'cancelled_at': ''})
chartmogul.Subscription.modify(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb' data={'cancellation_dates': []})
```

### [Metrics API](https://dev.chartmogul.com/docs/introduction-metrics-api)

Available methods in Metrics API:


```python
chartmogul.metrics.all(config, data={
  'start-date': '2015-01-01',
  'end-date': '2015-11-24',
  'interval': 'month',
  'geo': 'GB',
  'plans': 'Bronze Plan'
})
chartmogul.Metrics.mrr(config, data={},
                start_date='2015-01-01', # notice the _ here
                end_date='2015-11-24',
                interval='month',
                geo='GB',
                plans='PRO Plan')
chartmogul.Metrics.arr(config, data={})
chartmogul.Metrics.arpa(config, data={})
chartmogul.Metrics.asp(config, data={})
chartmogul.Metrics.customerCount(config, data={})
chartmogul.Metrics.customerChurnRate(config, data={})
chartmogul.Metrics.mrrChurnRate(config, data={})
chartmogul.Metrics.ltv(config, data={})

chartmogul.Activity.all(config, uuid='')
chartmogul.Subscription.all(config, uuid='')
```


### Errors

The library throws `chartmogul.APIError`.

## Development

To work on the library:

* Fork it
* Create your feature branch (`git checkout -b my-new-feature`)
* Install dependencies: `pip install -r requirements.txt && python setup.py develop`
* Fix bugs or add features. Make sure the changes pass the coding guidelines (use `pylama`).
* Write tests for your new features. Use `requests_mock` for HTTP mocking. Run tests with `python setup.py test` and check test coverage with `coverage run -m unittest discover --source=. && coverage report -m`
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

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
