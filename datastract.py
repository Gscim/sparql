from xml.dom import minidom 
import SPARQLWrapper as sw 
import json
import os

import logging
import logging.config
import time

log_filename = "logging.log"
logging.basicConfig(level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode='a')

graph = sw.SPARQLWrapper("http://162.105.146.140:3003/sparql")
graph.setReturnFormat(sw.JSON)

src_path = './qald-4_selected/'

for dirn in os.listdir(src_path):
    srcfile = open(src_path + dirn + '/answers.txt', 'r')
    resdict = {}
    findict = {}
    writedict = {}
    for entity in srcfile:
        queryhead = 'SELECT * WHERE { ' + entity.strip() + ' ?p ?uri }'
        try:
            graph.setQuery(queryhead)
            resdict['subj'] = entity.strip()
            results_ = graph.query().convert()['results']['bindings']
            results = []
            for v in results_:
                if v['uri']['type'] == 'literal':
                    resdict['obj'] = ('\"' + v['uri']['value'] + '\"' + '@' + v['uri']['xml:lang'])               
                elif v['uri']['type'][:5] == 'typed':
                    resdict['obj'] = ('\"' + v['uri']['value'] + '\"' + '^^' + '<' + v['uri']['datatype'] + '>')                    
                else:
                    resdict['obj'] = ('<' + v['uri']['value'] + '>')  

                if v['p']['type'] == 'literal':
                    resdict['pred'] = ('\"' + v['p']['value'] + '\"' + '@' + v['p']['xml:lang'])               
                elif v['p']['type'][:5] == 'typed':
                    resdict['pred'] = ('\"' + v['p']['value'] + '\"' + '^^' + '<' + v['p']['datatype'] + '>')                    
                else:
                    resdict['pred'] = ('<' + v['p']['value'] + '>')      

                results.append(resdict)
            findict['head'] = results
        except:
            continue

        querytail = 'SELECT * WHERE { ?uri ?p ' + entity.strip() + ' }'
        try:
            graph.setQuery(querytail)
            resdict['obj'] = entity.strip()
            results_ = graph.query().convert()['results']['bindings']
            results = []
            for v in results_:
                if v['uri']['type'] == 'literal':
                    resdict['subj'] = ('\"' + v['uri']['value'] + '\"' + '@' + v['uri']['xml:lang'])               
                elif v['uri']['type'][:5] == 'typed':
                    resdict['subj'] = ('\"' + v['uri']['value'] + '\"' + '^^' + '<' + v['uri']['datatype'] + '>')                    
                else:
                    resdict['subj'] = ('<' + v['uri']['value'] + '>')  

                if v['p']['type'] == 'literal':
                    resdict['pred'] = ('\"' + v['p']['value'] + '\"' + '@' + v['p']['xml:lang'])               
                elif v['p']['type'][:5] == 'typed':
                    resdict['pred'] = ('\"' + v['p']['value'] + '\"' + '^^' + '<' + v['p']['datatype'] + '>')                    
                else:
                    resdict['pred'] = ('<' + v['p']['value'] + '>')      

                results.append(resdict)
            findict['tail'] = results
        except:
            continue

        writedict[entity.strip()] = findict
    
    jfile = open("qald-4_selected/%d/related.json" % int(dirn), 'w')
    json.dump(writedict, jfile)
    logging.info("{} finished".format(dirn))

        
        
            





    
    




