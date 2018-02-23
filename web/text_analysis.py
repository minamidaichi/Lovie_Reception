# coding: utf-8
import MeCab

def tokenize(input_text):
    mt = MeCab.Tagger("-Ochasen")
    mt.parse('')
    node = mt.parseToNode(input_text)
    output_text = []
    while node:
        #print node.surface
        print node.feature
        if node.feature.split(",")[0] == "名詞":
            output_text.append(node.feature.split(",")[7])
        node = node.next
    return output_text
