## About

This Flask app is an experimental project to flesh out keywords in a Contentful content record. It takes keywords embedded in a jpeg image file uploaded to Contentful as a media asset and stores them in the linked Contentful content record(s).

## The intended use case / workflow

Working in the Contentful webapp, an editor attaches an image to go with the written content. On creation, the photographer / image creator had already tagged the image with keywords.

![alt text](https://raw.githubusercontent.com/jamessam/ctf-keyword-extractor-py/master/docs/screen_shots/IPTC_in_preview.png "IPTC data seen in macOS Preview")

Upon publishing the media asset, a webhook fires off a POST request to this app with the ASSET_ID value.

Because the content model includes a keywords list field on the original content entry, this app populates into Contentful the keywords the photographer had included.

![alt text](https://raw.githubusercontent.com/jamessam/ctf-keyword-extractor-py/master/docs/screen_shots/content_model_with_keywords.png "keywords seen in the Content Model")

The developer working on the project can now take those keywords for better SEO or other purpose.

## Prerequisites

* The image is in JPEG format.
* keywords embedded into the IPTC chunk of said JPEG image.
* A short text list in the Contentful content model with Field ID "keywords".

## Recommended architecture

The best way to get started with this project is to add it to AWS Lambda via the Zappa project. You'll need to have an AWS account, [install](https://docs.aws.amazon.com/cli/latest/userguide/installing.html) and [configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-quick-configuration) the AWS CLI tool, and [install and configure Zappa](https://github.com/Miserlou/Zappa). The documentation at Zappa is excellent and should be followed.
