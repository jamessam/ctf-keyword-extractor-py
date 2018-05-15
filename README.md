## About

This Flask app is an experimental project to flesh out keywords in a Contentful content record. It takes keywords embedded in a jpeg image file uploaded to Contentful as a media asset and stores them in the linked Contentful content record(s).

## The intended use case / workflow

Working in the Contentful webapp, an editor attaches an image to go with the written content. On creation, the photographer / image creator had already tagged the image with keywords.

![alt text](https://raw.githubusercontent.com/jamessam/ctf-keyword-extractor-py/master/docs/screen_shots/IPTC_in_preview.png "IPTC data seen in macOS Preview")

Upon publishing the media asset, a webhook fires off a POST request to this app.

The app calls all assets updated within the last 24 hours and cycles through them, looking at the linked entries of each asset.

If the content model includes a keywords list field on the original content entry, this app populates into Contentful the keywords the photographer had included. *To read the file's embedded metadata, it will download all the images*, so keep that in mind for billing/bandwidth reasons.

![alt text](https://raw.githubusercontent.com/jamessam/ctf-keyword-extractor-py/master/docs/screen_shots/content_model_w_keywords.png "keywords seen in the Content Model")

The developer working on the project can now take those keywords for better SEO or other purpose.

## Prerequisites

* The image is in JPEG format.
* keywords embedded into the IPTC chunk of said JPEG image.
* A short text list in the Contentful content model with Field ID "keywords".

## Recommended architecture

Due to the intermittent nature of this process, leveraging AWS Lambda makes a ton of sense.

To quickly get started with this project and Lambda is to use the Zappa project. It will configure much of AWS for you. You are free to upload to the Lambda and configure API Gateway yourself should you choose to.

To use Lambda and Zappa, you'll need to have an AWS account, [install](https://docs.aws.amazon.com/cli/latest/userguide/installing.html) and [configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-quick-configuration) the AWS CLI tool, and [install and configure Zappa](https://github.com/Miserlou/Zappa). The documentation at Zappa is excellent and should be followed.

## Test images note
All images were downloaded from StockSnap.io and are believed to be free of copyright restrictions. Should you be the rights holder and this is not the case, please raise an issue on GitHub ASAP.
