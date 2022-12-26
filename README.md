# Gun Violence and Mass Shooting in America (2019 - 2022)
### December 2022

## Abstract
This project provides an analysis on mass shootings in America from October 2019 through December 2022 including a Shiny for Python application for user exploration. Data was sourced primarily from the [Gun Violence Archive (GVA)](https://www.gunviolencearchive.org/), as well as [State Firearm Laws](https://www.statefirearmlaws.org/) and the [US Census](https://www.census.gov/) American Community Survey 2016-2020 5 year estimate. GVA methodology employs a purely statistical threshold to define mass shooting based on the numeric value of <b> 4 or more shot or killed, not including the shooter</b>. 
<br>
The analysis found the following during the data's time span:

- Most states had less than one mass shooting per 1,000 people, however there where a few outliers namely:
    - Washington DC
    - Louisana
    - Illinois
    - Mississippi
    - Delaware
    - South Carolina
- When controlling per 1,000 population, Washington DC became an extreme outlier, with only ~700,000 living within city limits and greater than 4 mass shooting incidents per 1,000 people.
- Average injured per 1,000 people per incident, was more then 4 times kiled per 1,000 people.
- Most frequent day and month for mass shootings events were Sunday and August respectively.
- The summer season also had the most mass shooting events.
- Weekends were also more violent per mass shooting event the weekdays on average by .5 injured and killed per incident
- Increased quantity of Gun laws did not express any significant corelation with a reduction in mass shootings
- States with NO mass shooting incidents during the timeframe of the data were:
    - Vermont, North Dakota and Wyoming
- Overall, states in the southeastern region (i.e. Louisana, Missippi, South Carolina) along with Illinois and Delaware, had the most frequent occurences of mass shooting incidents per 1,000 people

## Shiny for Python app Link

[Mass Shootings in the US (2019 - 2022)](https://justinm0rgan.shinyapps.io/gun-violence-mass-shooting-us/)

## Next Steps
- Extend analysis on Gun Laws
- Zoom in on Metro areas i.e. NYC, LA and Chicago
- Larger sample size (expand on how data collection techniques changed for GVA in 2019)
- Add additional tabs to Shiny application with summary statistics
- Improve visual appearence and performance of app

