# COVID Visualization Dashboard

<!-- [![shiny-deploy](https://github.com/UBC-MDS/covid_viz/actions/workflows/deploy-app.yaml/badge.svg)](https://github.com/UBC-MDS/covid_viz/actions/workflows/deploy-app.yaml) -->

<!-- The dashboard is hosted on `shinyapps.io`, please click the link [here](https://jenitj61.shinyapps.io/covid_viz/) -->

## Author

-   Jenit Jain

## Link to the app

https://covid-dash-app.onrender.com

## Overview 

This repository hosts the dasboard for COVID-19 data released by [*Our World in Data*](https://ourworldindata.org/coronavirus) which is present in the this [repository](https://github.com/owid/covid-19-data/tree/master/public/data) and are completely open access under the [Creative Commons BY license](https://creativecommons.org/licenses/by/4.0/). The motivation, purpose, description of data and research question can be found in our [proposal](https://github.com/UBC-MDS/covid_viz/blob/main/reports/proposal.md).

## Usage 

This Dash based python dashboard is designed to provide travelers with COVID-19 information for them to assess their risk of contacting the disease while traveling to different countries. The dashboard has been designed to give the user flexibility to view the rise in daily cases and the stringency of the COVID-19 policies applied by different countries using various filtering options. If users are interested to know if countries with similar characteristics have similar COVID-19 statistics, they can used the slider to filter countries based on their GDP and population. There is also a date slider in the bottom of the dashboard to allow users to select a date interval if they are interested in knowing the progress of the pandemic in its earlier stages.

The 2 types of visualizations included are:
- A line plot showing the change in the stringency index of a country over time, which reflects the strictness of government response due to the pandemic. 
- A bar graph showing the top countries with the highest daily cases. 

*The brief questions answered by this dashboard would be:* 
- As a traveler one would want to know the current COVID stringency situation at the destination country.
- Study the impact of COVID on different countries based on GDP and population.
- Study a particular country based on timeline to see how it was impacted over the months due to COVID.

<br>

<!-- # Dashboard Demo

![](img/ezgif.com-video-to-gif.gif) -->

## Get involved 

**How to run the app locally and make contributions**

If you would like to contribute to our project, please read the CONTRIBUTING.md file and then follow these steps: 
- Ensure that you have python3 installed on your computer.
- Fork the repository and [clone](https://github.com/brabbit61/covid_viz.git) it onto your computer.
- Create a new branch (named according to the specifications in the CONTRIBUTING.md file).

 *To run the app locally:* 

- Navigate to the source directory of the repository on the location machine.
- Ensure all the necessary packages are installed:

    `pip3 install -r requirements.txt`

- Execute the following command in a bash terminal:

    `python3 app.py`

*To propose new changes:* 
- Fork the repository
- Make your changes to the code in VSCode and adhere to best coding practices. 
- Commit your changes (with an informative commit message).
- Push your changes to your fork - Submit a pull request.

**Places for improvement** 
- Build upon the current map plot and add interactive elements to the plot. 

## Contributing 

Interested in contributing? Check out the [contributing guidelines](CONTRIBUTING.md). Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License 

`covid_viz` was created using Dash visualization by Jenit Jain. It is licensed under the terms of the [MIT license](LICENSE).

## References

- [Our World in Data](https://ourworldindata.org/coronavirus)
- [Dataset](https://github.com/owid/covid-19-data/tree/master/public/data)