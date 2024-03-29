# Branches

Please note that the `main` branch corresponds to the UPDOWN and NEUTRAL competitions that run on the test `YIEDL` token.

For the ROCKET competition that ran on the `MUSA` token, please switch to the `musa_competition` branch.


### This repository hosts the Quickstart jupyter notebook for Rocket Capital Investment (RCI) competitions which is meant to run on Google Colab.
#### For more details, please visit [our documentation page](https://docs.rocketcapital.ai/rci-competition/submission-guide).

- To launch the Quickstart.ipynb, you may access via https://colab.research.google.com/github/rocketcapital-ai/competition_quickstart_dataloader/blob/main/Quickstart.ipynb.
- The Quickstart.ipynb downloads latest dataset from IPFS. It then show an example of workflow to load the data, building the features (X) and target (y), split data in to train and test set, applying machine learning algorithm to build a regression model, generate prediction, and preparing a dataframe for submission. The prediction.csv can be used to participating RCI competition using decentralized application (DAPP) at https://rocketcapital.ai/dapp/
- Files description:
	- Quickstart.ipynb --> quick start guide to generate prediction for competition.
	- dataloader.py --> library used download competition dataset from ipfs.

## IPFS Gateway URL
Due to the lower speed of public IPFS gateways and the [deprecation] of Infura's higher-performing public IPFS gateways, users now need to specify their own IPFS gateway url for retrieving the dataset.
IPFS gateway urls, as well as pinning services, are available from various providers.
Users are encouraged to obtain a (free) IPFS gateway url from [Infura](https://infura.io/).

### Steps to obtain gateway url and continue running the scripts in this repo
1. Open an Infura account and obtain a dedicated Infura IPFS gateway url according to [this](https://docs.infura.io/infura/networks/ipfs/how-to/access-ipfs-content/dedicated-gateways).
2. Make sure that "Pinned Content Only" is **not checked**.
3. In `Quickstart.ipynb`, paste your new url into the `my_gateway` variable in the first cell. <br>Your url should be of the form "https://*custom-subdomain*.infura-ipfs.io"

### Pinata Access Token
If using a pinata dedicated gateway, you will need to add an access token from your pinata settings, copy it and then paste that into the `pinata_access_token` field.