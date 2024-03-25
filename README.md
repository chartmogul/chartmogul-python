<p align='center'>
<a href='https://chartmogul.com'><img width='200' src='https://user-images.githubusercontent.com/5329361/42206299-021e4184-7ea7-11e8-8160-8ecd5d9948b8.png'></a>
</p>

<h3 align='center'>Official ChartMogul API Python Client</h3>

<p align='center'><code>chartmogul-python</code> provides convenient Python bindings for <a href='https://dev.chartmogul.com'>ChartMogul's API</a>.</p>
<p align='center'>
  <a href="https://badge.fury.io/py/chartmogul"><img src="https://badge.fury.io/py/chartmogul.svg" alt="PyPI version" height="18"></a>
  <a href='https://travis-ci.org/chartmogul/chartmogul-python'><img src='https://travis-ci.org/chartmogul/chartmogul-python.svg?branch=main' alt='Build Status'/></a>
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

This library requires Python 3.8 to 3.12. It was last tested against Python 2.7 in version 1.3.0.

```sh
pip3 install chartmogul
```

## Configuration

First create a `Config` object by passing your API key, available from the administration section of your ChartMogul account.
You need to pass this configuration object as the first argument to each request.

```python
import chartmogul
config = chartmogul.Config('api_key')
```

Alternatively, you can use the library without the module prefix:
```python
from chartmogul import *
config = Config('api_key')
```

Note that both ways should import all necessary classes and submodules,
but the first one is preferred due to being explicit.

To test authentication, try ping endpoint:
```python
import chartmogul
chartmogul.Ping.ping(config).get()
```
This throws error or returns `<Ping{data='pong!'}>`

### Options
You can also pass to the Config initializer:
* `request_timeout=` sets timeout for requests (seconds), default: none (see [requests docs](https://2.python-requests.org/en/master/user/quickstart/#timeouts) for details)

### Rate Limits & Exponential Backoff
The library will keep retrying if the request exceeds the rate limit or if there's any network related error.
By default, the request will be retried for 20 times (approximately 15 minutes) before finally giving up.

You can change the retry count from the Config initializer:

 * `max_retries=` sets the maximum number of retries for failed requests, default: 20
 * `backoff_factor=` sets the exponential backoff factor, default: 2

Set max_retries 0 to disable it.
Set backoff_factor 0 to disable it.

## Usage

The library is based on [promises](https://pypi.python.org/pypi/promise) (mechanism similar to futures).
Every call therefore returns an object like `<promise.promise.Promise object at 0x123456789>`
The requests are running asynchronously, but you can use them synchronously, just appending `.get()`,
which will block your program until the response has come.
Both sync/async ways will return/pass native Python objects mapping to the entities in the API,
or raise/pass errors from the API, see an example:

```python
import chartmogul

config = chartmogul.Config('api_key')
req = chartmogul.Plan.create(config, data={'name': 'Awesome plan'...})

# Now either asynchronous reaction:
req.then(lambda plan: print(plan)).catch(reactOnException)

# or synchronous:
try:
    print(req.get())
except Exception as ex:
    reactOnException(ex)
```

### Import API

Available methods in Import API:

#### [Data Sources](https://dev.chartmogul.com/docs/data-sources)

```python
chartmogul.DataSource.create(config, data={'name': 'In-house billing'})
chartmogul.DataSource.retrieve(config, uuid='ds_5915ee5a-babd-406b-b8ce-d207133fb4cb')
chartmogul.DataSource.all(config)
chartmogul.DataSource.destroy(config, uuid='ds_5915ee5a-babd-406b-b8ce-d207133fb4cb')
```

#### [Customers](https://dev.chartmogul.com/docs/customers)

```python
chartmogul.Customer.create(config, data={})
chartmogul.Customer.all(config, cursor='cursor==', per_page=20)
chartmogul.Customer.retrieve(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb')
chartmogul.Customer.search(config, email='email@email.com')
chartmogul.Customer.merge(config, data={
  'from': {'customer_uuid': 'cus_5915ee5a-babd-406b-b8ce-d207133fb4cb'},
  'into': {'customer_uuid': 'cus_2123290f-09c8-4628-a205-db5596bd58f7'}
})
chartmogul.Customer.modify(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb', data={
  "city": "San Francisco",
  "country": "US",
  "state": "CA",
})
chartmogul.Customer.destroy(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb')
chartmogul.Customer.connectSubscriptions(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb', data={
  'subscriptions': [
    {
      "data_source_uuid": "ds_ade45e52-47a4-231a-1ed2-eb6b9e541213",
      "external_id": "d1c0c885-add0-48db-8fa9-0bdf5017d6b0"
    },
    {
      "data_source_uuid": "ds_ade45e52-47a4-231a-1ed2-eb6b9e541213",
      "external_id": "9db5f4a1-1695-44c0-8bd4-de7ce4d0f1d4"
    }
  ]
})
chartmogul.Customer.contacts(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb', cursor='aabbcc', per_page=20)
chartmogul.Customer.createContact(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb', data={})
chartmogul.Customer.notes(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb', cursor='aabbcc', per_page=20)
chartmogul.Customer.createNote(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb', data={})
chartmogul.Customer.opporunities(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb', cursor='aabbcc', per_page=20)
chartmogul.Customer.createOpportunity(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb', data={})
```

#### [Contacts](https://dev.chartmogul.com/docs/contacts)

```python
chartmogul.Contact.create(config, data={})
chartmogul.Contact.all(config, cursor='aabbcc', per_page=20)
chartmogul.Contact.retrieve(config, uuid='con_5915ee5a-babd-406b-b8ce-d207133fb4cb')
chartmogul.Contact.merge(config, into_uuid='con_5915ee5a-babd-406b-b8ce-d207133fb4cb', from_uuid='con_2123290f-09c8-4628-a205-db5596bd58f7')
chartmogul.Contact.modify(config, uuid='con_5915ee5a-babd-406b-b8ce-d207133fb4cb', data={
  "email": "test@example.com"
})
chartmogul.Contact.destroy(config, uuid='con_5915ee5a-babd-406b-b8ce-d207133fb4cb')
```

#### [Customer Notes](https://dev.chartmogul.com/docs/customer_notes)
```python
chartmogul.CustomerNote.create(config, data={})
chartmogul.CustomerNote.all(config, cursor='aabbcc', per_page=20, customer_uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb')
chartmogul.CustomerNote.retrieve(config, uuid='note_5915ee5a-babd-406b-b8ce-d207133fb4cb')
chartmogul.CustomerNote.patch(config, uuid='note_5915ee5a-babd-406b-b8ce-d207133fb4cb')
chartmogul.CustomerNote.destroy(config, uuid='note_5915ee5a-babd-406b-b8ce-d207133fb4cb')
```

#### [Opportunities](https://dev.chartmogul.com/docs/opportunities)

```python
chartmogul.Opportunity.create(config, data={})
chartmogul.Opportunity.all(config, cursor='aabbcc', per_page=20, customer_uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb')
chartmogul.Opportunity.retrieve(config, uuid='5915ee5a-babd-406b-b8ce-d207133fb4cb')
chartmogul.Opportunity.patch(config, uuid='5915ee5a-babd-406b-b8ce-d207133fb4cb')
chartmogul.Opportunity.destroy(config, uuid='5915ee5a-babd-406b-b8ce-d207133fb4cb')
```

#### [Customer Attributes](https://dev.chartmogul.com/docs/customer-attributes)

Note that the returned attributes of type date are not parsed and stay in string.

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
chartmogul.Plan.all(config, cursor='cursor==', external_id='')
chartmogul.Plan.destroy(config, uuid='')
```

#### [Plan Groups](https://dev.chartmogul.com/docs/plan_groups)

```python
chartmogul.PlanGroup.create(config, data={})
chartmogul.PlanGroup.retrieve(config, uuid='plg_5915ee5a-babd-406b-b8ce-d207133fb4cb')
chartmogul.PlanGroup.modify(config, uuid='plg_5915ee5a-babd-406b-b8ce-d207133fb4cb', data={})
chartmogul.PlanGroup.all(config, cursor='cursor==')
chartmogul.PlanGroup.all(config, uuid='plg_5915ee5a-babd-406b-b8ce-d207133fb4cb')
chartmogul.PlanGroup.destroy(config, uuid='')
```

#### [Invoices](https://dev.chartmogul.com/docs/invoices)

```python
import chartmogul

chartmogul.Invoice.create(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb', data={})
chartmogul.Invoice.all(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb', cursor='cursor==', per_page=10)
chartmogul.Invoice.all(config, customer_uuid='cus_f466e33d-ff2b-4a11-8f85-417eb02157a7', external_id='INV0001')
chartmogul.Invoice.retrieve(config, uuid='inv_22910fc6-c931-48e7-ac12-90d2cb5f0059')
```

#### [Transactions](https://dev.chartmogul.com/docs/transactions)

```python
import chartmogul

chartmogul.Transaction.create(config, uuid='inv_745df1d4-819f-48ee-873d-b5204801e021', data={})
```

#### [SubscriptionEvents](https://dev.chartmogul.com/docs/subscription_events)

```python
import chartmogul
chartmogul.SubscriptionEvent.all(config)
chartmogul.SubscriptionEvent.create(config, data={
  'subscription_event' : {
    'external_id' : 'evnt_026',
    'customer_external_id' : 'scus_022',
    'data_source_uuid' : 'ds_1fm3eaac-62d0-31ec-clf4-4bf0mbe81aba',
    'event_type' : 'subscription_start_scheduled',
    'event_date' : '2022-03-30',
    'effective_date' : '2022-04-01',
    'subscription_external_id' : 'sub_0001',
    'plan_external_id' : 'gol d_monthly',
    'currency' : 'USD',
    'amount_in_cents' : 1000,
    'quantity': 1
}})
chartmogul.SubscriptionEvent.modify_with_params(config, data={
'subscription_event' : {
    'id' : 73966836,
    'currency' : 'EUR',
    'amount_in_cents' : 100
}})
chartmogul.SubscriptionEvent.destroy_with_params(config, data={
'subscription_event' : {
    'id' : 73966836
}})
```

#### [Subscriptions](https://dev.chartmogul.com/docs/subscriptions)

```python
import chartmogul

chartmogul.Subscription.list_imported(config, uuid='cus_5915ee5a-babd-406b-b8ce-d207133fb4cb')
chartmogul.Subscription.cancel(config, uuid='sub_3995ee5a-bbdb-406b-a8ca-d207133fb9bb' data={'cancelled_at': ''})
chartmogul.Subscription.modify(config, uuid='sub_3995ee5a-bbdb-406b-a8ca-d207133fb9bb' data={'cancellation_dates': []})
```

### [Metrics API](https://dev.chartmogul.com/docs/introduction-metrics-api)

Available methods in Metrics API:


```python
chartmogul.Metrics.all(config,
                       start_date='2015-01-01', # notice the _ here
                       end_date='2015-11-24',
                       interval='month',
                       geo='GB',
                       plans='Bronze Plan'
)
chartmogul.Metrics.mrr(config,
                       start_date='2015-01-01',
                       end_date='2015-11-24',
                       interval='month',
                       geo='GB',
                       plans='PRO Plan')
chartmogul.Metrics.arr(config, data={})
chartmogul.Metrics.arpa(config, data={})
chartmogul.Metrics.asp(config, data={})
chartmogul.Metrics.customer_count(config, data={})
chartmogul.Metrics.customer_churn_rate(config, data={})
chartmogul.Metrics.mrr_churn_rate(config, data={})
chartmogul.Metrics.ltv(config, data={})

chartmogul.CustomerActivity.all(config, uuid='')
chartmogul.CustomerSubscription.all(config, uuid='cus_cf121bf8-db58-11ec-8575-43bda9fb67ad')
chartmogul.Activity.all(config, start_date='2020-06-02T00:00:00Z')

chartmogul.ActivitiesExport.create(config,data={})
chartmogul.ActivitiesExport.create(config, data={'type':'churn', 'start-date':'2020-06-02T00:00:00Z'})
chartmogul.ActivitiesExport.retrieve(config, id='febbd467-40d4-4f99-a647-3f47333453db')
```

### Account

Available methods:

```python
chartmogul.Account.retrieve(config)
```


### Errors

The library throws `TypeError` if data parameter is not serializable.

The `chartmogul.ArgumentMissingError` is raised if obligatory `uuid` or `data`
is missing in the call.

The error `chartmogul.APIError` is raised for any non-20x response from the API.
It always has cause of type `requests.HTTPError`, which contains the response,
so you can extract JSON/text in the following way (and program reaction):

```python
from pprint import pprint
try:
    chartmogul.doStuff()
except chartmogul.APIError as e:
    response = e.__cause__.response
    try:
        pprint(response.json())
    except ValueError:
        pprint(response.text)
```

The cause default serialization doesn't give the API user much detail:
```
HTTPError('422 Client Error: Unprocessable Entity for url: https://api.chartmogul.com/v1/data_sources',)
```

That's why it's wrapped, so that you get the detail by default.
```
APIError(b'{"errors":{"name":"Has already been taken."}}',)
```

## Development

To work on the library:

* Fork it
* Create your feature branch (`git checkout -b my-new-feature`)
* Setup a virtual environment (`python -m venv <directory>`)
* Activate the virtual environment (`source <directory>/bin/activate`)
* Install dependencies: `pip3 install -r requirements.txt && python3 setup.py develop`
* Fix bugs or add features. Make sure the changes pass the coding guidelines (use `pylama`).
* Write tests for your new features. Use `requests_mock` for HTTP mocking.
  * To run test install requirement-test `pip3 install -r requirements-test.txt` and run with `python -m unittest`:
    * `pip3 install coverage`
    * `coverage run ./setup.py test`
    * `coverage html --include='chartmogul/*'`
    * Find results in `htmlcov/index.html`
* If all tests are passed, push to the branch (`git push origin my-new-feature`)
* Create a new Pull Request

For a testing project we recommend setting up a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
with [development mode](https://packaging.python.org/installing/#installing-from-a-local-src-tree) installation
and [Jupyter](http://jupyter.org/). [virtualenvwrapper](http://chrisstrelioff.ws/sandbox/2014/09/04/virtualenv_and_virtualenvwrapper_on_ubuntu_14_04.html) is another handy tool.

Built using [Requests](https://github.com/kennethreitz/requests).

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/chartmogul/chartmogul-python.

## Releasing

Make sure that:
1. you have prepared `~/.pypirc` with credentials,
2. a higher version has been set in `chartmogul/__init__.py`,
3. Test & build package `python3 setup.py test sdist`
4. release works `twine upload --repository-url https://test.pypi.org/legacy/ dist/*`,
5. release to production `twine upload dist/*`,

[Read full HOWTO](http://peterdowns.com/posts/first-time-with-pypi.html)

## License

The library is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).

### The MIT License (MIT)

*Copyright (c) 2016 ChartMogul Ltd.*

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
