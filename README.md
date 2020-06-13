# Medeina

Medeina is a python package for automating the construction of species interaction webs, such as food webs, or pollination webs. [X] The package allows both management of a data store of interactions, and functions needed to make use of the data store in building a cumulative interaction web. Medeina comes with a pre-loaded data store of 2,740,185 interactions, coming from 38,865 unique species- one of the largest interaction web stores online. Here is the list..

The project comes from a refactoring of a larger networks project at the University of Bristol.

#  Features

## The Web Class

For creating species interaction webs, you will a list of species from your environment. The project will standardise these names for you, by using the EcoNameTranslator[]. The species names can be in any format- whether scientific species name, scientific names at higher taxonomic ranks, or common English name (although this should be used with caution). Under the hood, Medeina translates these forms to scientific species names when matching possible interactions. 

Medeina also works at higher levels of taxonomy: you may specify a taxonomic rank, which will dictate to what similarity interaction matching happens. For example, consider that the various Gannet birds eat the various Cod fish types. Each Gannet, e.g. the Northern Gannet (\textit{Morus bassanus}), or Cape Gannet (\textit{Morus capensis}), doesn’t necessarily discriminate between Pacific cod (\textit{Gadus macrocephalus}), or Atlantic Cod (\textit{Gadus morhua}), etc. Even if the interaction data store doesn't contain the link between a Northern Gannet and a Pacific Cod- having an observation containing a Northern Gannet and an Atlantic Cod might be enough indication that such a link likekly exists. If a researcher is prepared to accept such inferred links, then the network created at the end of the process may be far richer. 

When the cumulative interaction web has been computed, it can be interpreted as either a list of tuples of the form (predator,prey), a numpy matrix, or a networkx object.

## The WebStore 

If you would like to add your own interaction dataset to Medeina, you can do so with the WebStore object. CSV file formats are taken, and your data may be in list format (where each row is an individual interaction), or a matrix.

# Quick Examples

## Building an interaction web out-of-the-box
```python
from EcoNameTranslator import EcoNameTranslator
unstandardised_names = ['Panhera tigris'] #Should be "Panthera tigris"       
translator = EcoNameTranslator()   
index = translator.translate(unstandardised_names)
print(index)
# {'Panera tigris':['panthera tigris']}    
```

commit back:

- getDId function
- mention relying on the API as bad; e.g. bryozoa returning all the way down to family
