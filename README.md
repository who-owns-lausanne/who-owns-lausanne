# Who owns Lausanne?

## Abstract
Why are rents in Lausanne so expensive? And who profits from it?

The real estate market is usually quite opaque to the public. Being ourselves
residents of Lausanne, we know how hard finding affordable housing can be.
Therefore we would like to know more about the market situation that causes
these difficulties. Our goal is to analyse cadastral and rental data in order to
find and visualise the ownership proportions of real estate in the city of
Lausanne and to understand how prices are composed.

More precisely, by leveraging public-domain data from the administration of both
the city of Lausanne and the _canton de Vaud_ we attempt to relate real estate
owners and high cost of rents. Furthermore, we try to understand the data from a
political point of view. Thereby we hope to improve the transparency of the real
estate situation and its effects – _for the good of our society._

Our results are narrated as a data story on the website
[who-owns-lausanne.github.io](http://who-owns-lausanne.github.io)

## Repo contents

This repository contains all the code and documentation about the project "who
owns Lausanne". The following directory structure helps you while exploring:

- `/cleaning`: This folder contains scripts that are used to clean some datasets
  after they have been acquired.

- `/data`: Load all the data in this folder. All the scripts expect the data to
  be contained there. This folder has the following subfolders:
    - `maps` contains the geographical data
    - `raw` contains scraped data before it is cleaned,
    - `owners` contains the data about the ownership of parcels
    - `rents` contains the data about current rent announcements
    - `xlsx_commune` features some spreadsheets from the statistical office of
        the city of Lausanne.

- `/scraping`: Contains all scripts needed to get data from the different web
  services.

- `/Who owns lausanne.ipynb`: The main notebook featuring data analysis and
  explanations. This is your next chapter after this document.

## Research questions

- **How does the position influence rent prices?** Property and rent prices vary
  greatly with position within Switzerland. Is the same true also within the
  city of Lausanne? Are any neighbourhoods significantly cheaper or more
  expensive depending on their distance from the centre?

- **How does the type of owners influence prices** Several categories of owners
  are invested in the real estate market: private citizens, companies, pension
  funds, and public institutions. We ask ourselves whether the proportions of
  these categories influence rent prices. For example, is a certain part of the
  city more expensive because most real estate there is possessed by companies?

- **Does the position influence the composition of property owners?** As
  position might influence prices, it could also influence the profile of real
  estate investors. We look for the way in which position influences the
  composition of the categories of owners. As mentioned before, this is highly
  related to the dependence of prices and location.

#### Analysis by _quartier_

Our analysis will use the _quartiers_ (districts) of the city of Lausanne as
a natural spatial unit.
Lausanne is divided, for geographical and historical reasons, in
[18 _quartiers_][quartier].
From a data science position, one might say that this
unit is far too large and one might be inclined to use a finer grid in order to perform the analysis.

However, if we remind ourselves of the goal of this project, it is to help
society understand a problem: how are rent prices composed? As human beings we
are used to think of a place by its political divisions like the districts of a
city. If someone is asked where in the town they live the usual answer will be
the name of the _quartier_. The same should be true _if someone asks, where in
the city the rents are affordable_. Therefore, we will use this conventional
division to perform our analysis and to showcase our story.

[quartier]:https://www.lausanne.ch/officiel/statistique/quartiers/presentation-des-quartiers.html

## Story outline

We want to turn this project into a story that will be told on a nicely
designed webpage. The story will take the perspective of someone trying to find
accommodation in Lausanne, think of a newly arrived student.

Driven by the difficulties of finding an affordable home in Lausanne, we start
asking the question: Who owns all this real estate? And why are the rents in
some _quartiers_ cheaper than in others? Following this, there will
be an analysis of the ownership patterns overall and for different _quartiers_.
Where are the most big companies etc. (see research questions).

The main part of the story will explain our findings about the composition
of prices in different _quartiers_. It will combine the knowledge from the
previous part and it will bring all the calculations together. We hope to
be able to give an explanation whether the distance from the centre or the
ownership pattern influences the price and where a newly arrived student should
search for affordable accommodation.

The entire story will feature various maps showing for example the ownership
patterns or the differences in rent prices.

## Datasets

Even though our datasets are not listed on the site
[opendata.swiss](https://opendata.swiss), we still consider them to be "open
swiss data". They come from official swiss administrations or swiss
websites/webservices and they are **open to the public**.

#### Cadastral data

The basis for our analysis is the cadastral data which is published by the city
of Lausanne on [map.lausanne.ch](https://map.lausanne.ch). It features
information for each parcel including the owner, the area, and the position. The
dataset is described on
[asitvd.ch](https://www.asitvd.ch/chercher/catalogue.html?view=sheet&guid=486&catalog=main&type=complete&preview=search_list).
Here is an example screenshot and data for the Bel-Air building in the centre of
Lausanne:

![Bel-Air](belair.png)

The cadastral dataset is available for free for research institutions. We
contacted the _service du secrétariat général et cadastre_ of the city of
Lausanne on Friday, 2 November. They gave us the access to their `ftp` server.

#### Address data

We also need to convert addresses to coordinates at some point. There is luckily
another cadastral layer of building addresses, provided by the Cadastral offic
of Lausanne. It can again be found on the `ftp` server.

#### Maps of the _quartiers_

To be able to capture the space-dependent behaviour of rent prices and ownership
structure, we will need to aggregate our data by position. As said before, we
will use the official _quartiers_ delimitation of the city  of Lausanne. The
[reference
map](https://www.google.com/maps/d/u/0/viewer?mid=1Fhi7wXjxdSfkNnZSwMysrh0JPQD2BLMF&ll=46.55355566379154%2C6.652336000000105&z=12)
is hosted on Google Maps. It is possible to download it as a KML file.

#### Rent prices

To collect data points on the cost of rent in Lausanne, we retrieved the current
listings for rents from three websites:
[anibis](https://www.anibis.ch/fr/default.aspx),
[homegate](https://www.homegate.ch/fr) and [tutti](https://tutti.ch). We were
able to download about 900 offers from Anibis, 400 from Homegate and 600 from
Tutti. The data needed extensive cleaning to select only offers for which the
address is known and valid, and the surface area of the offer's object is
available. Entries present in all datasets were detected and deduplicated.


## Implementation

#### Sourcing the data
Getting our hands on the required data was already a challenging aspect of this
project. Several scrapers were developed for this purpose. The Jupyter notebook
describes the scraping and cleaning phase.

#### Data pipeline

The total datasets size is under 1 GB. We can therefore run all of our analysis
on a single local machine.

At the source, the cadastral data of Lausanne is available in ShapeFile format.
The _quartiers_ boundaries are in KML format. The rent offers are in the raw
formats used by the respective website's UI. To process the spatial data in a
coherent way in Python, we converted the ShapeFile and KML files to GeoJson by
using the [QGIS software application](https://www.qgis.org/en/site/). Ad-Hoc
parsers were needed for the rent offers data.

#### Model

The main analysis goal of this project is to determine how prices vary as a
function of the ownership pattern of a _quartier_ and as a function of the
_quartier_'s distance from the centre. In order to do this, we will use a
linear regression model that is detailed in the notebook. We hope that this
will reveal information about price composition of rents.

## Further ideas and discussion

Having now a clear line (the calculation and estimation of the prices in the
_quartiers_ of Lausanne) guiding us through our project, we can assess what
benefit the project can make of certain datasets. Clearly, we needed some
additional rental data in order to estimate the mean rent of a _quartier_.
This data was obtained by scraping some of the most used websites for real
estate announcements in Switzerland (anibis.ch, homegate.ch and tutti.ch).
Together with the ownership data we already had this completes our needs for
the regression model.

There were additional ideas that came up during our discussions of the model
and the story we wanted to tell. Some of them are listed here. For most of them
we won't have the time and data. But if (for some miracle) there is still time
we might want to use one of them:

- During our research we stumbled upon some statistics done by the statistical
  office of the city of Lausanne. They contain similar data as the results
  of our analysis (rental prices by _quartiers_, etc.) However they date back
  to the year 2000. Nonetheless, it could be interesting to compare our results
  in the end to those from 2000.

- Rating the quality of life in each _quartier_ by counting the number of shops,
  restaurants, bars, bus stops and the like. This could be done using the Google
  Maps API. The life quality factor would then be another covariate in the
  regression model. However, coming up with the scoring function is very
  complicated.

- Estimating the real estate surface of the buildings using the data for
  building heights extracted from a [LIDAR](https://en.wikipedia.org/wiki/Lidar)
  scan of the canton. We already mentioned this in the last milestone and the
  dataset is also described on
  [asitvd.ch](https://www.asitvd.ch/chercher/catalogue.html?view=sheet&guid=553&catalog=main&type=complete&preview=search_list).

- Another idea was to cluster the parcels without a notion of _quartiers_.  
  However, as described before _quartiers_ are a very meaningful and human
  delimiters. Also, we weren't sure how such a clustering result would have to
  be interpreted for our analysis and what we could deduce from it for our
  story.

## Individual Contributions

- __Jonathan Besomi__:
   - responsible for the Jupyter Notebook
   - scraped tutti.ch for rent offers
   - price extrapolation with K-nearest neighbours on parcelles

- __Yann Bolliger__:
    - wrote text/concept for project proposal
    - scraped Homegate for rent offers
    - linear regression on distance and surface
    - designed website
    - wrote data-story

- __Pietro Carta__:
    - sourced the cadastral dataset from the Lausanne office of cadastre
    - scraped the missing details of the cadastral dataset
    - explored the cadastral dataset with QGIS
    - scraped anibis for rent offers
    - matched rent offers to geographical positions and owners
    - linear regression on price depending on owner type
    - denoised the owner types map
