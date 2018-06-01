from xml.dom import minidom
import SPARQLWrapper as sw
import json
import os

graph = sw.SPARQLWrapper("http://162.105.146.140:3003/sparql")  # endpoint
graph.setReturnFormat(sw.JSON)
i = 1
os.mkdir("qald-4_selected")

tree = minidom.parse("./qald-4_multilingual_train_withanswers.xml")  # xml file 1
root = tree.documentElement
questions = root.getElementsByTagName('question')
for question in questions:
    if question.getAttribute('aggregation') == 'false' and question.getAttribute('answertype') == 'resource':
        query = question.getElementsByTagName('query')[0]
        textnode = query.childNodes[0]
        if textnode.data != "OUT OF SCOPE":
            query_dict = {'query': textnode.data, 'answers': set()}
            answers = question.getElementsByTagName('answers')[0].getElementsByTagName('answer')
            if len(answers[0].getElementsByTagName('uri')) == 0:
                continue
            try:
                graph.setQuery(textnode.data)
                results_ = graph.query().convert()['results']['bindings']
                results = []
                for v in results_:
                    if v['uri']['type'] == 'literal':
                        results.append('\"' + v['uri']['value'] + '\"' + '@' + v['uri']['xml:lang'])               
                    elif v['uri']['type'][:5] == 'typed':
                        results.append('\"' + v['uri']['value'] + '\"' + '^^' + '<' + v['uri']['datatype'] + '>')                    
                    else:
                        results.append('<' + v['uri']['value'] + '>')
                #results = {v['uri']['value'] for v in results}
            except:
                continue
            os.mkdir("qald-4_selected/%d" % i)
            query = textnode.data
            fq = open("qald-4_selected/%d/query.txt" % i, 'w')
            fq.write(query)
            fq.close()
            fa = open("qald-4_selected/%d/answers.txt" % i, 'w')
            for result in results:
                fa.write(result)
                fa.write('\n')
            fa.close()
            i += 1
tree = minidom.parse("./qald-4_multilingual_test_withanswers.xml")  # xml file 2
root = tree.documentElement
questions = root.getElementsByTagName('question')
for question in questions:
    if question.getAttribute('aggregation') == 'false' and question.getAttribute('answertype') == 'resource':
        query = question.getElementsByTagName('query')[0]
        textnode = query.childNodes[0]
        if textnode.data != "OUT OF SCOPE":
            query_dict = {'query': textnode.data, 'answers': set()}
            answers = question.getElementsByTagName('answers')[0].getElementsByTagName('answer')
            if len(answers[0].getElementsByTagName('uri')) == 0:
                continue
            try:
                graph.setQuery(textnode.data)
                results_ = graph.query().convert()['results']['bindings']
                result = []
                for v in results_:
                    if v['uri']['type'] == 'literal':
                        results.append('\"' + v['uri']['value'] + '\"' + '@' + v['uri']['xml:lang'])
                    elif v['uri']['type'][:5] == 'typed':
                        results.append('\"' + v['uri']['value'] + '\"' + '^^' + '<' + v['uri']['datatype'] + '>')
                    else:
                        results.append('<' + v['uri']['value'] + '>')
                #results = {v['uri']['value'] for v in results}
            except:
                continue
            os.mkdir("qald-4_selected/%d" % i)
            query = textnode.data
            fq = open("qald-4_selected/%d/query.txt" % i, 'w')
            fq.write(query)
            fq.close()
            fa = open("qald-4_selected/%d/answers.txt" % i, 'w')
            for result in results:
                fa.write(result)
                fa.write('\n')
            fa.close()
            i += 1