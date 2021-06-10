# Hotel Booking Analysis Dashboard Using Flask

## About the Data
The hotel booking demand dataset is originally from the article Hotel Booking Demand Datasets, written by Nuno Antonio, Ana Almeida, and Luis Nunes for Data in Brief, Volume 22, February 2019. The data was downloaded and cleaned by Thomas Mock and Antoine Bichat for #TidyTuesday during the week of February 11th, 2020.<br>
This data set contains booking information for a city hotel and a resort hotel, includes information such as when the booking was made, length of stay, the number of adults, children, and/or babies, and the number of available parking spaces, among other things. All personally identifying information has been removed from the data.<br>

## Context Analysis
This hotel booking demand dataset is ideal for anyone looking to practice their exploratory data analysis (EDA), cause you can be employed descriptive analytics to further understand patterns, trends, and anomalies in the data such as:<br>
1. Knowing the distribution of the guest's origin country
2. Finding out when is the best time of year to book a hotel room (to get the best daily rate),
3. Estimating when booking times have many cancellations (so the losses arising from the cancellation can be overcome).
<br>You can start by completing this dashboard which is intended for the needs of travel agents and hotels management.

## Data Summary
- `Hotel`:
    - H1: Resort hotel
    - H2: City hotel
- `is_canceled`: Value indicating if the booking was canceled (1) or not (0)
- `lead_time`: Number of days that elapsed between the entering date of the booking into the PMS and the
- `stays_in_weekend_nights`: Number of weekend nights (Saturday or Sunday) the guest stayed or booked to stay at the hotel
- `stays_in_week_nights`: Number of week nights (Monday to Friday) the guest stayed or booked to stay at the hotel
- `adults, children, babies`: Number of adults, children, and babies
- `country`: Country of origin. Categories are represented in the ISO 3155–3:2013 format
- `adr`: Average Daily Rate as defined by dividing the sum of all lodging transactions by the total number of staying nights
- `arrival_date`: arrival (check-in) date

## Dependencies
- Flask
- Plotly
- Pandas
- Numpy
