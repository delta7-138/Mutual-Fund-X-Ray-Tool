# **Mutual Fund 'X-RAY'Tool**
## **Problem Faced** ##
---
## **Project Idea** ##
**Aim** : Building a diagnostic X-Ray tool for analysing performance of mutual funds at a glance. 

**Focus** : is on Equity-linked Savings schemes(commonly referred to as 'tax saving' mutual fund schemes) in India.

**Types Of Schemes** : Regular (invested through agents) and Direct (invested directly by investors)


## **Tech Stack** ##
**django** : The python module django was used to host a web application, the front end of which used *boostrap* and *google api fonts*

**pandas** : The python module pandas was used to extract data from downloaded Excel files containing the NAVs(net asset values) of the schemes. (Link of which is mentioned in references). 

**openpyxl** : This python module was used to compile the results of the analysis in an Excel file, which can be downloaded using  the web app.
 
**datetime** : This module was used to increment date objects 

## **Progress of the project** ##
- As of now, the user can select a scheme after which one can choose the start date and end date. 
- An excel file for the performance of the selected scheme can be thus downloaded. 
- This Excel File contains all the statistical quantities and ratios calculated as a result of a mathematical analysis on the raw data. 
- One file can be downloaded one at a time.
- There are 50 schemes as of now which can be analysed. 
- They can only be analysed for a duration between 01-10-2014 and   
27-12-2019

## **Future Prospects** ##
## **References** ##

