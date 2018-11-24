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

## Research questions

 - **Who owns Lausanne?** Our title defines the primary aim of this project:
 - getting insights into the ownership of real estate in Lausanne.

 - **What proportion of real estate is possessed by companies,    privates,
   etc.?** In Switzerland there are a particularly high number of privately
   possessed flats (_ownership of an entire floor_, _propriété par étages_ in
   french). Is this fact visible in the data for Lausanne? Or are there many
   real estate objects possessed by companies?

 - **What proportion of real estate is possessed by non-swiss entities?** This
   question builds on the previous one. Especially for company owned objects it
   might be interesting to see whether those companies are based in Switzerland
   or in other countries.

 - **Who are the richest private real estate owners? How are they involved in
   local/cantonal politics?** Consider for example the _Flon_ in the centre of
   Lausanne. Most buildings there are indirectly owned by a company called
   "Mobimo AG". Georges Theiler is a member of their administrative board and at
   the same time he's active in the liberal democratic party of Switzerland
   (_PLR_).

## Datasets

Even though our datasets are not listed on the site
[opendata.swiss](https://opendata.swiss), we still consider them to be "open
swiss data". They come from official swiss administrations or swiss
websites/webservices and they are **open to the public**.

##### Data sources

The basis for our analysis is the cadastral data which is published by the city
of Lausanne on [map.lausanne.ch](https://map.lausanne.ch). It features
information for each parcel including the owner, the area, and the position. The
dataset is described on
[asitvd.ch](https://www.asitvd.ch/chercher/catalogue.html?view=sheet&guid=486&catalog=main&type=complete&preview=search_list).
Here is an example screenshot and data for the Bel-Air building in the centre of
Lausanne:

![Bel-Air](belair.png)

<!-- TODO: Johnny: Change this paragraph for the scraping -->

If we'll need more detailed information, we might also aggregate data from real
estate portals like [anibis.ch](https://anibis.ch) and
[homegate](https://www.homegate.ch/).

<!-- TODO: Johnny: Change this for todays perspective where we have the data -->

The cadastral dataset is available for free for research institutions. We
contacted the _service du secrétariat général et cadastre_ of the city of
Lausanne on Friday, 2 November. They gave us the access to their `ftp` server.

##### Technical details

We estimate the size of the composite datasets to be of several hundred MB at
most. Therefore, it will comfortably fit into the memory of a single machine.

Regarding the first dataset, the [map.lausanne.ch](https://map.lausanne.ch) API
returns `XML` formatted data. The second dataset is available in several
[GIS](https://en.wikipedia.org/wiki/Geographic_information_system) formats, such
as MIF/MID (MapInfo), Shapefile, and DXF.

Although our datasets are of geographical nature, we should be able to perform
much of the processing without the need of geographical databases. We can, for
example, find the most important real estate owners by simply ranking them by
number of parcels owned. To refine the analysis, however, we might want to
include information about the building's surface area and position in our
evaluation model. This would require a finer utilisation of geographical data.

## Story outline

We want to turn this project into a story that will be told on a nicely
designed webpage. The story will take the perspective of someone trying to find
accommodation in Lausanne, think of a newly arrived student. Maybe we will even
invent an imaginary character and tell the story from his/her point of view.

Driven by the difficulties of finding an affordable home in Lausanne, we start
asking the question: Who owns all this real estate? And why are the rents in
some _quartiers_ (districts) cheaper than in others? Following this, there will
be an analysis of the ownership patterns overall and for different _quartiers_.
Where are the most big companies etc. (see research questions).

The main part of the story will then explain our findings about the composition
of prices in different _quartiers_. It will combine the knowledge from the
previous part and it will bring all the calculations together. We hope to
be able to give an explanation whether the distance from the centre or the
ownership pattern influences the price and where a newly arrived student should
search for affordable accommodation.

The entire story will feature various maps showing for example the ownership
patterns or the differences in rent prices.


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
