#!/usr/bin/env python3

import yaml
import requests
import sys
import subprocess
from html.parser import HTMLParser


class ProcessCollections():
    '''Parses Collections from the datastore at https://data.legumeinfo.org'''

    def __init__(self, datastore_url="https://data.legumeinfo.org"):
        self.collections = []  # get collections for writing site
        self.datastore_url = datastore_url  # URL to search for collections
        self.out_dir = "/var/www/html/jbrowse_autodeploy"  # out dir for jbrowse2 tracks
        self.files = {}  # get types for making jbrowse2
        self.collection_types = ["genomes", "annotations", "diversity", "expression",
                                 "genetic", "markers"]  # types to search for

    def parse_attributes(self, response_text):  # inherited from Sammyjava 
        '''parses attributes returned from HTMLParser'''
        collections = []
#        relationships = {'genomes': {}, 'annotations': {}}  # establish related objects

        class CollectionsParser(HTMLParser):
            '''HTMLParser for Collections'''

            def handle_starttag(self, tag, attrs):
                '''Feed from HTMLParser'''
                for attr in attrs:
                    if((attr[0]=='href' and "/annotations/" in attr[1])
                            or (attr[0]=='href' and "/diversity/" in attr[1])
                            or (attr[0]=='href' and "/expression/" in attr[1])
                            or (attr[0]=='href' and "/genetic/" in attr[1])
                            or (attr[0]=='href' and "/genomes/" in attr[1])
                            or (attr[0]=='href' and "/markers/" in attr[1])):
                        collections.append(attr[1])
        CollectionsParser().feed(response_text)  # populate collections
        self.collections = collections  # set self.collections

    def get_attributes(self, parts):
        '''parse parts return url components'''
        gensp = f'{parts[1].lower()[:3]}{parts[2][:2]}'  # make gensp
        strain = parts[-2]  # get strain and key information
        return (gensp, strain)

    def deploy_jbrowse2(self, out_dir="/var/www/html/jbrowse_autodeploy"):
        '''deploy jbrowse2 from collected objects'''
        self.out_dir = out_dir
        for collectionType in self.collection_types:
            for file in self.files[collectionType]:
               # jbrowse add-assembly -a alis -n "full name" --out /path/to/jbrowse2 URL
                cmd = ''
                url = self.files[collectionType][file]['url']
                name = self.files[collectionType][file]['name']
                genus = self.files[collectionType][file]['genus']
                parent = self.files[collectionType][file]['parent']
                species = self.files[collectionType][file]['species']
                infraspecies = self.files[collectionType][file]['infraspecies']
                if collectionType == 'genomes':
                    cmd = f'jbrowse add-assembly -a {name} --out {self.out_dir}/ -t bgzipFasta'
                    cmd += f' -n "{genus.capitalize()} {species} {infraspecies} {collectionType.capitalize()}" {url}'
                if collectionType == 'annotations':
                    cmd = f'jbrowse add-track -a {parent} --out {self.out_dir}/'
                    cmd += f' -n "{genus.capitalize()} {species} {infraspecies} {collectionType.capitalize()}" {url}'
                print(cmd)
                if subprocess.check_call(cmd, shell=True):
                    print("ERROR: {cmd}")

    def parse_collections(self, target="../_data/taxon_list.yml"):
        '''Retrieve and output collections for jekyll site'''    
        taxonList = yaml.load(open(target, 'r').read(),
                                   Loader=yaml.FullLoader)  # load taxon list
        for taxon in taxonList:
            if not 'genus' in taxon:
                print('ERROR GENOME REQUIRED: {taxon}')  # change to log
                sys.exit(1)
            genus = taxon['genus']
            genusDescriptionUrl = f'{self.datastore_url}/{genus}/GENUS/about_this_collection/description_{genus}.yml'
            genusDescriptionResponse = requests.get(genusDescriptionUrl)
            if genusDescriptionResponse.status_code==200:  # Genus Description yml SUCCESS
                genusDescription = yaml.load(genusDescriptionResponse.text, Loader=yaml.FullLoader)
                speciesCollectionsFilename = "../_data/taxa/"+taxon["genus"]+"/species_collections.yml"  # change this to fstring
                speciesCollectionsFile = open(speciesCollectionsFilename, 'w')
                print('---', file=speciesCollectionsFile)
                print('species:', file=speciesCollectionsFile)
                for species in genusDescription["species"]:
                    print("### "+taxon["genus"]+" "+species)
                    print('- '+'name: '+species, file=speciesCollectionsFile)
                    speciesUrl = f'{self.datastore_url}/{genus}/{species}'
                    for collectionType in self.collection_types:
                        if collectionType not in self.files:  # add new type
                            self.files[collectionType] = {}
                        print('  '+collectionType+':', file=speciesCollectionsFile)
                        collectionsUrl = speciesUrl+"/"+collectionType+"/"
                        collectionsResponse = requests.get(collectionsUrl)
                        if collectionsResponse.status_code==200:  # Collections SUCCESS
                            self.collections = []
                            self.parse_attributes(collectionsResponse.text)  # Feed response from GET
                            for collectionDir in self.collections:
                                parts = collectionDir.split('/')
#                                print(parts)
                                name = parts[4]
                                url = ''
                                parent = ''
                                parts = self.get_attributes(parts)
                                lookup = f"{parts[0]}.{'.'.join(name.split('.')[:-1])}"  # reference name in datastructure
                                if(collectionType == 'genomes'):  # add parent genomes
                                    url = f'{self.datastore_url}{collectionDir}{parts[0]}.{parts[1]}.genome_main.fna.gz'
                                if(collectionType == 'annotations'):
                                    genome_lookup = '.'.join(lookup.split('.')[:-1])  # grab genome
                                    self.files['genomes'][genome_lookup]['url']
                                    parent = genome_lookup
                                    url = f'{self.datastore_url}{collectionDir}{parts[0]}.{parts[1]}.gene_models_main.gff3.gz'
                                self.files[collectionType][lookup] = {'url': url, 'name': lookup, 'parent': parent,
                                                                      'genus': genus, 'species': species,
                                                                      'infraspecies': parts[1]}  # add type and url
#                                print(f'this thing {self.files}')
                                readmeUrl = f'{self.datastore_url}/{collectionDir}README.{name}.yml'
                                readmeResponse = requests.get(readmeUrl)
                                if readmeResponse.status_code==200:
                                    readme = yaml.load(readmeResponse.text, Loader=yaml.FullLoader)
                                    synopsis = readme["synopsis"]
                                    print('    - collection: '+name, file=speciesCollectionsFile)
                                    print('      synopsis: "'+synopsis+'"', file=speciesCollectionsFile)
                                else:  # README FAILURE
                                    print(f'GET Failed for README {readmeResponse.status_code} {readmeUrl}')  # change to log
#                                    sys.exit(1)
                        else:  # Collections FAILUTRE
                            print(f'GET Failed for collections {collectionsResponse.status_code} {collectionsUrl}')  # change to log
#                            sys.exit(1)
            else:  # FAILURE
                print(f'GET Failed for genus {genusDescriptionResponse.status_code} {genusDescriptionUrl}')  # change to log
#                sys.exit(1)


if __name__ == '__main__':
    parser = ProcessCollections()
    parser.parse_collections()
    parser.deploy_jbrowse2()
