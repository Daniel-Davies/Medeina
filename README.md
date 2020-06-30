# Medeina

Medeina is a python package for automating the construction of species interaction webs, such as food webs, or pollination webs.The package allows both management of a data store of interactions, and functions needed to make use of the data store in building a cumulative interaction web. For convenience, Medeina comes with a pre-loaded data store of 2,740,185 interactions, coming from 38,865 unique species, which is de-compressed and readily available from the first use. A list of the datasets that come native with Medeina can be found [here](https://github.com/Daniel-Davies/MedeinaPublicationTests) under 'dataset_lists'.

#  Features

## The Web Class

For creating species interaction webs, you will need a list of species from your environment. The project will standardise these names for you, by using the [EcoNameTranslator package](https://pypi.org/project/EcoNameTranslator/) (a slightly more powerful version of the R taxize package). The species names can be in any format- whether scientific species name, scientific names at higher taxonomic ranks, or common English name (although this should be used with caution). Under the hood, Medeina translates these forms to scientific species names when matching possible interactions. 

You may also specify a taxonomic rank, which will dictate to what extent similarity of species can be used to infer interactions, which can help you find interaction store data undersampling. The default is exact string name matching, but you may also specify Genus, Family, Class, Order, Phylum and Kingdom.

When the cumulative interaction web has been computed, it can be interpreted as either a list of tuples, a numpy matrix, or a networkx object.

## The WebStore 

If you would like to add your own species interaction dataset to Medeina, you can do so with the WebStore object. CSV file formats are taken, and your data may be in list format (where each row is an individual interaction), or a matrix. The names in your interaction dataset are also parsed and translated to scientific species names for Medeina to use. Take a look at the official documentation() for examples of how to add datasets in a range of formats.

# Quick Examples

## Building an interaction web out-of-the-box
```python
from Medeina import Web
w = Web()       
species_data = ['Panthera Tigris','Gazelle', 'Equus']
result = w.apply(species_data)
print(result.to_list())
# [('Panthera Tigris','hello')...]
```

## Tailoring the interaction data store

```python
from Medeina import Web
web = Web()
pollination_web = 
    web.filter_by_interaction_type(  
        ["pollination"]
    )
british_pollination_web = 
    pollination_web.filter_by_country(
        ["United Kingdom"]
    )
...   
result = british_pollination_web.apply(
            species=[...]
         )
result = w.apply(species_data)
print(result.to_list())
# [('Panthera Tigris','hello')...]
```

## Adding your own interaction data
```python
from Medeina import WebStore
store = WebStore()
# Specify data properties
dct = {}
dct['source'] = 'Davies(2020)'
...
dct['encoding'] = {}
dct['encoding']['interactionFormat'] = 'pair'
dct['encoding']['head'] = 'Predator'
dct['encoding']['tail'] = 'Prey'
dct['encoding']['evidencedBy'] = 'Evidence'
dct['encoding']['path'] = "C:/Users/..."
# Read, Index, and Add Interactions
store.add_interactions(dct)
# For exporting data from the WebStore
store.export_data(path="C:/Users/...", \ 
                  datasets=[2,4..])
```


## Auditing links
```python
from Medeina import Web
w = Web()       
species_data = ['Panthera Tigris','Gazelle', 'Equus']
result = w.apply(species_data)
# A csv of the links, meta data,
#  and the original links that led to 
# the inference
result.audit("C:/...")  
```