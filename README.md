# Gun Violence and Mass Shooting in America (2019 - 2022)
### December 2022

## Summary
This project provides an analysis on mass shootings in America from October 2019 through December 2022 and includes a Shiny for Python application for user exploration. Data was sourced primarily from the [Gun Violence Archive (GVA)](https://www.gunviolencearchive.org/), as well as [State Firearm Laws](https://www.statefirearmlaws.org/) and the [US Census](https://www.census.gov/) American Community Survey 2016-2020 5 year estimate. GVA methodology employs a purely statistical threshold to define mass shooting based on the numeric value of <b> 4 or more shot or killed, not including the shooter</b>. 
<br>
<br>
The analysis found the following:

Most states had less than one mass shooting per 1,000 people, however there where a few outliers namely:
- Washington DC
- Louisana
- Illinois
- Mississippi
- Delaware
- South Carolina

States with no mass shooting incidents were:
- Vermont
- North Dakota
- Wyoming

When controlling per 1,000 population, Washington DC with only ~700,000 living within city limits and greater than 4 mass shooting incidents per 1,000 people, became an extreme outlier. The average injured per 1,000 people per incident, was more then 4 times killed per 1,000 people. The most frequent day and month for mass shootings events were Sunday and August. Overall, on average weekends were more violent per mass shooting event then the weekdays by .5 injured and killed per incident, while the summer season had the most mass shooting events. All this said, increased quantity of Gun laws did not show any significant corelation with a reduction in mass shootings incidents.

Overall, southeastern states Louisiana, Mississippi, South Carolina, as well as Illinois and Delaware, had the most frequent occurences of mass shooting incidents per 1,000 people.

## Shiny for Python app Link

[Mass Shootings in the US (2019 - 2022)](https://justinm0rgan.shinyapps.io/gun-violence-mass-shooting-us/)

## Next Steps

Would like to extend the analysis on correlation with Gun Laws and quantity of mass shooting events. In addition, would like to zoom in and focus on a few metro areas i.e. NYC, LA and Chicago at the county level. This would enable a more detailed look at differing socio-economic features and their possible contribution to mass shooting events. Would also like to add additional content through tab layout, as well as improving performance and visual appearence of Shiny app. 


