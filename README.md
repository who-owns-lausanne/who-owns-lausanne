# Who owns Lausanne?

## Abstract
**Subject and social good.**

## Research questions
 - **Who owns Lausanne?**
  Our title already gives the primary question we want to answer with our project. The goal is however not to simply condense the data to a single name. Our goal is to visualise and analyse the ownership of real estate under different perspectives.


 - **What proportion of real estate is possessed by companies,    privates, etc.?**
  In Switzerland there are a particularly high number of privately possessed flats (_ownership of an entire floor_,
  _propriété par étages_ in french). Is this fact visible in the data for Lausanne?
  Or are there many real estate objects possessed by companies?
  We will also try to compare the different proportions to Swiss average values.

 - **What proportion of real estate is possessed by non-swiss entities?**
  This question builds on the previous one. Especially for company owned objects it might be interesting to see if those companies are based in Switzerland or in other countries.

 - **Who are the richest private real estate owners? How are they involved in local/cantonal politics?**
  Consider for example the _Flon_ in the centre of Lausanne. Most buildings there are indirectly owned by a company called "Mobimo AG". Georges Theiler is a member of their administrative board and at the same time is active in the liberal democratic party of Switzerland (_PLR_).

## Dataset
**--> open swiss data but not on opendata.swiss**

The basis for our analysis is the data which is published by the land cadastre of the city of Lausanne on [map.lausanne.ch](map.lausanne.ch).
It features information for each parcel including the owner, the area, and the position. The dataset is described on [this page](https://www.asitvd.ch/chercher/catalogue.html?view=sheet&guid=486&catalog=main&type=complete&preview=search_list).
Here is an example screenshot and data for the Bel-Air building in the centre of Lausanne:

![Bel-Air](belair.png)

Additionally, we might want to want to estimate the real estate surface of the buildings. This is not in the dataset above. However, we can use the data for building heights extracted from a LIDAR scan of the canton. This dataset is also described on [asitvd.ch](https://www.asitvd.ch/chercher/catalogue.html?view=sheet&guid=553&catalog=main&type=complete&preview=search_list).

Both datasets are available for free for research institutions.
We contacted the _service du secrétariat général et cadastre_ of the city of Lausanne on Friday, 2 November.
They confirmed that the data is available for free for students – in general. However, the responsible person was out of office and will reach back to us on Monday.

We esteem the size of the composite datasets to be of several hundred MB at most, therefore, it will comfortably fit within the memory of a single machine.
Regarding the first dataset, the map.lausanne.ch API returns xml formatted data, but the format for the bulk data export still needs to be negotiated with the owners.
The second dataset is available in several [GIS](https://en.wikipedia.org/wiki/Geographic_information_system) formats, such as MIF/MID (MapInfo), Shapefile, DXF.
Although our datasets are of geographical nature, we should be able to perform much of our processing without the need of geographical databases.
We can, for example, find the biggest owners by simply ranking them by number of parcels owned.
To refine the analysis, however, we could want to include informations about the buildings surface area and position in our evaluation model, which would require a finer utilization of geographical data.

## A list of internal milestones up until project milestone 2
Add here a sketch of your planning for the next project milestone.

## Questions for TAs
Add here some questions you have for us, in general or project-specific.
