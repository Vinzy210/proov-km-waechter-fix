# What I checked, and what the agent got wrong

I noticed that the agent found several bugs in the existing code. One important and major bug was using the // insetead of / .Because of this 14,900 km out of 15,000km was incorrectly treated as havin 0% wear. 

## What the agent got wrong
I also checked the handling of cars where last_service_km was missing.These cars shouldn't have treated automatically as if they were being serviced at 0 km.

## What I checked before I accepted its work
I checked that the service interval was still 15,000km and that the warning threshold still set to 80%.The agent changed how the percentage was calculated, but it did not change the actual rules. A car is still marked for service when its wear reaches or goes above 80% of the 15,000km service interval.

## What the data actually said
The analysis clearly showed that the "avg_daily_km" and "load_factor" were the main factors that showed the difference between cars that broke down and card that didn't.The average daily kms increased from 131-160 and the load factor increased from 0.50 to 0.60.On the other hand "odometer_km" and "age_years" were almost te same for both groups so they weren't the strong predictors in this dataset.
