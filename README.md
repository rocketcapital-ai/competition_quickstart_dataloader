### This repository hosted the Quickstart jupyter notebook for Rocket Capital Investment (RCI) competition which is meant to run on Google Colab.
#### For more detail, please visit https://rocket-capital-investment.gitbook.io/rci-competition/

- To launch the Quickstart.ipynb, you may access via https://colab.research.google.com/github/rocketcapital-ai/competition_quickstart_dataloader/blob/main/Quickstart.ipynb.
- The Quickstart.ipynb downloads latest dataset from IPFS. It then show an example of workflow to load the data, building the features (X) and target (y), split data in to train and test set, applying machine learning algorithm to build a regression model, generate prediction, and preparing a dataframe for submission. The prediction.csv can be used to participating RCI competition using decentralized application (DAPP) at https://rocketcapital.ai/dapp/
- Files description:
	- Quickstart.ipynb --> quick start guide to generate prediction for competition.
	- dataloader.py --> library used download competition dataset from ipfs.