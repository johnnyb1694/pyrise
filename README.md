# `pyrise` - A Daily Planning Service :sunrise:

## Introduction

A minimalist personal assistant that helps me to plan my day :relaxed:

`pyrise` sends me a scheduled email every morning at 6:30am (GMT) with the following information,

- Recipes to try out when the evening comes along! :bento: :pizza:
- A 'stoic' quote of the day

There is scope to add more to this service in the future.

Here is a sample:

<img src="docs/email-sample.png" alt="drawing" width="500"/>

## Deployment

This service is deployed to AWS,

* The email handler is deployed to Lambda
* Access tokens are parsed via S3
* EventBridge is used to invoke the service on a scheduled basis





