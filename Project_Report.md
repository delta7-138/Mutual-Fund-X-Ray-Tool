# **Mutual Fund 'X-RAY'Tool**
## **Problem Faced** ##
- The requirement of a mutual fund schemes tool for calculation of **absolute risk-adjusted measures** for mutual fund schemes.

---
## **Project Idea** ##
**Aim** : Building a diagnostic X-Ray tool for analysing performance of mutual funds at a glance. 

**Focus** : is on Equity-linked Savings schemes(commonly referred to as 'tax saving' mutual fund schemes) in India.

**Types Of Schemes** : Regular (invested through agents) and Direct (invested directly by investors)

---
## **Tech Stack** ##
**django** : The python module django was used to host a web application, the front end of which used *boostrap* and *google api fonts*

**pandas** : The python module pandas was used to extract data from downloaded Excel files containing the NAVs(net asset values) of the schemes. (Link of which is mentioned in references). 

**openpyxl** : This python module was used to compile the results of the analysis in an Excel file, which can be downloaded using  the web app.
 
**datetime** : This module was used to increment date objects 

**urllib** : This module was used to send request to the api website and collect json files

**json** : To collect the json files from the Free India Mutual Fund API.

---
## **Progress of the project** ##
- As of now, the user can select a scheme after which one can choose the start date and end date. 
- An excel file for the performance of the selected scheme can be thus downloaded. 
- This Excel File contains all the statistical quantities and ratios calculated as a result of a mathematical analysis on the raw data. 
- One file can be downloaded one at a time.
- There are 50 schemes as of now which can be analysed. 
- They can only be analysed for a duration between 01-10-2014 and   
27-12-2019.

---
## **Future Prospects** ##

- A multi-step drawdown can be added to cover all the categories and sub-categories of mutual fund schemes
- A second level filter can be added to compare and chart the performance of multiple schemes.
---
## **References** ##

### *Mentorship and Background details* ###
1. Beyond the mandatory information available to retail mutual investors on the measures , viz. point to point absolute returns, 3-year Sharpe ratios , etc.), the extent of publicly available tools that provide deep insights on ‘Absolute Risk- Adjusted Returns’ are not significant to make informed decisions. 

2. The project was conducted under the **mentorship** of an ***investment advisory firm (WealthSecrets)*** that helped build an understanding of the most appropriate performance measures to be included in the MF X-Ray Tool. As such, these are the most preferred measures for financial analysts and savvy investors globally in analyzing the performance of financial assets/investment decisions.

### *Links to resources* ###

3. [openpyxl documentation](https://openpyxl.readthedocs.io/en/stable/)

4. [Stack Overflow](https://stackoverflow.com/) for further understanding the modules used.

5. [Django documentation](https://docs.djangoproject.com/en/3.0/)

6. [Datetime documentation](https://docs.python.org/3/library/datetime.html)

7. [Bootstrap CDN source](https://getbootstrap.com/docs/3.3/getting-started/)

8. [Google Fonts](https://fonts.google.com/)

9. [Free India Mutual Fund API](https://www.mfapi.in/) to access NAV of schemes over a period of time

### Link to Demonstration Video ###

**[Demo Video](https://drive.google.com/open?id=19wv3OGOTkNJTQSQ_oDAIpwPgct2X45kA)**


### **Absolute Risk Measures** ###
>**Standard Deviation** : Measures the variation of a scheme’s returns around its arithmetic mean return for the considered period. The higher the volatility of the returns, the higher the standard deviation. And higher the perceived risk. 
>
>**Geometric standard deviation** : Measures the variation of a scheme’s returns around its geometric mean return for the considered period. The higher the volatility of the returns, the higher the geometric standard deviation. And higher the perceived risk. describes how spread out are a set of numbers whose preferred average is the geometric mean.
>
>**Downside Deviation**: It considers the variation of only returns that fall below a defined minimum acceptable return (MAR). 
>
>**For the purpose of this analysis , the MARs considered were**:
> 
> 1. Zero('0'): That is returns that are zero or negative. Suited for investors who are looking for funds with a track record of minimal rolling period returns below zero.
> 
> 2. 0.5 percent(30 day)/19.10%(1095 day) : Suited for investors who are looking for funds with a track record of minimal rolling period returns below six per cent annually that they would otherwise get by investing in risk free government bonds, liquid funds, bank fixed deposits.
> 
> 3. 0.67 percent(30 day)/25.97 percent(1095 day) : Suited for investors who are looking for funds with a track record of minimal rolling period returns below eight per cent annually that they would expect their savings to grow in line with inflation.
> 
>**Down Period Percent** : Number of rolling returns periods that were below ‘0’ percent return, divided by the total number of periods observed in the date range. 
>
>**Underperformance Percent**: Number of rolling returns periods that were below ‘6’ percent annual return, divided by the total number of periods observed in the date range
> 0.5% for 30 day rolling returns
>
> 19.10% for 1095 day rolling returns 
>
>**Geometric coefficient of variation(GCV)** :     • Also known as relative standard deviation (RSD), it is a standardized measure of dispersion of a probability distribution or frequency distribution. To obtain the geometric coefficient of variation, we reduce the geometric standard deviation to the power of the reciprocal of the geometric mean.
>
>The higher the GCV, the greater the level of dispersion around the mean. So conversely, a lower GCV is preferred by investors.

---

### Absolute Risk-adjusted measures ###
>**Sharpe Ratio**: A measure of a fund’s return relative to its risk. The numerator is defined as the fund’s incremental average return (Arithmetic Mean/Geometric Mean) over the risk-free rate. The risk (denominator) is defined as the Standard Deviation/Geometric Standard Deviation of the fund’s returns.
>
>**Sortino Ratio**:Another measure of a fund’s return relative to its risk. However, unlike the Sharpe Ratio, it the fund’s incremental average return (Arithmetic Mean/Geometric Mean) over the risk-free rate over a minimum acceptable return (MAR), and the risk (denominator)  is defined  as the downside  deviation below the MAR. 
>
>**Omega**: A measure of the likelihood of the scheme achieving a target MAR. It is a ratio of the cumulative probability of an investment’s outcome above an investor’s MAR, divided by the cumulative probability of an investment’s outcome below the MAR. The higher the omega value for a MAR, the greater the probability that the MAR return will be met or exceeded by the scheme.

---