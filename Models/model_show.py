#coding:utf-8
import tensorflow as tf
import json
import collections
from datetime import datetime
def model_show(path_name):
    checkpoint_path = 'prune_model/' + path_name + '/model.ckpt-0'
    log_path = 'prune_model/' + path_name + '/' + path_name + '_log.txt'
    out_file = open(log_path, 'w')
    ckpt_reader = tf.train.NewCheckpointReader(checkpoint_path)
    ckpt_vars = ckpt_reader.get_variable_to_shape_map().keys()
    ckpt_vars.sort()
    for var in ckpt_vars:
        #print var
        out_file.write(var + '\n')
        #print ckpt_reader.get_tensor(var).shape
        a = ckpt_reader.get_tensor(var).shape
        out_file.write(str(a) + '\n')
    return log_path
def compare_2_conv(log_prune,log_original):
    file_1 = open(log_prune,'r+')
    lines = file_1.readlines()
    aa = []
    w_main = []
    w_next = []
    w_other = []
    num = 0
    for line in lines:
        temp = line
        aa.append(temp)
        num = num+1
    file_2 = open(log_original,'r+')
    lines = file_2.readlines()
    bb = []
    for line in lines:
        temp = line
        bb.append(temp)
    i = 0
    while aa[i]:
        aa[i] = aa[i].strip('\n')
        bb[i] = bb[i].strip('\n')
        if aa[i]!=bb[i]:
            aa[i] = aa[i].replace(' ','')
            aa[i] = aa[i].replace('(', '')
            aa[i] = aa[i].replace(',',' ')
            aa[i] = aa[i].replace('\n','')
            aa[i] = aa[i].replace(')','')
            if aa[i].split(' ')[-1] =='':
                aa[i] = aa[i][:-1]
            bb[i] = bb[i].replace(' ','')
            bb[i] = bb[i].replace('(', '')
            bb[i] = bb[i].replace(',',' ')
            bb[i] = bb[i].replace('\n','')
            bb[i] = bb[i].replace(')','')
            if bb[i].split(' ')[-1] =='':
                bb[i] = aa[i][:-1]
            # [-1] not equal -> weights main/weights other
            if aa[i].split(' ')[-1]!=bb[i].split(' ')[-1]:
                if (str(aa[i - 1]).split('/')[-1]).strip('\n') == str('weights').strip('\n'):
                    #print "case 1:  weight main"
                    #print aa[i - 1]
                    #print aa[i]
                    w_main.append(aa[i-1])
                else :
                    #print "case 2:  weights other"
                    #print aa[i - 1]
                    #print aa[i]
                    w_other.append(aa[i-1])
            # [-2] not equal -> weights next
            else :
                if aa[i].split(' ')[-2]!=bb[i].split(' ')[-2]:
                    #print "case 3:  weights next"
                    #print aa[i - 1]
                    #print aa[i]
                    w_next.append(aa[i-1])
        i = i+1
        if i+1 == num:
            break
    return w_main,w_next,w_other
def write_weights(path_name,w_main,w_next,w_other):
    with open(path_name + '_output.txt', "a+") as outfile:
        conv_name = path_name.split('_')[0]
        outfile.write()
        len_main = len(w_main)
        len_other = len(w_other)
        len_next = len(w_next)
        i = 0
        outfile.write("\t")
        outfile.write("{'weight_other_list':'")
        while w_other[i]:
            outfile.write(str(w_other[i]))
            outfile.write(",")
            outfile.write("\\")
            outfile.write("\n")
            i = i + 1
            if i == len_other:
                outfile.write(str(w_other[i - 1]))
                outfile.write("'.split(','),")
                outfile.write("\n")
                break
        i = 0
        outfile.write("\t")
        outfile.write("'weight_main_list':'")
        while w_main[i]:
            outfile.write(str(w_main[i]))
            outfile.write(",")
            outfile.write("\\")
            outfile.write("\n")
            i = i + 1
            if i == len_main:
                outfile.write(str(w_main[i - 1]))
                outfile.write("'.split(','),")
                outfile.write("\n")
                break
        i = 0
        outfile.write("\t")
        outfile.write("'weight_next_list':'")
        while w_next[i]:
            outfile.write(str(w_next[i]))
            outfile.write(",")
            outfile.write("\\")
            outfile.write("\n")
            i = i + 1
            if i == len_next:
                outfile.write(str(w_next[i - 1]))
                outfile.write("'.split(','),")
                outfile.write("\n")
                break
        outfile.write("\t")
        outfile.write("},")
def json_weights(path_name,w_main,w_next,w_other):

    key = str(path_name).split('_')[0]
    value = {'weight_main_list':w_main,'weight_other_list':w_other,'weight_next_list':w_next}
    dic = {key : value}
    #print dic
    #return key,value
    return dic
if __name__ == '__main__':
    print "step 1: compute original conv:"
    model_show('model_original')
    log_original = model_show('model_original')
    print "step 2: compute prune conv: input 0 to stop"
    network_name = {}
    network_name = collections.OrderedDict()
    while 1:
        path_name = raw_input("       Input conv layer name:  ")
        if path_name!="0":
            model_show(path_name)
            log_prune = model_show(path_name)
            #print "step 3: compare 2 convs:"
            compare_2_conv(log_prune, log_original)
            #print "step 4: output of weights:"
            w_main, w_next, w_other = compare_2_conv(log_prune, log_original)
            json_weights(path_name,w_main,w_next,w_other)
            dic = json_weights(path_name,w_main,w_next,w_other)
            #print "step 5: merge json of weights:"
            network_name.update(dic)
        else :
            if path_name=="0":
                break
    #print network_name
    jsons = json.dumps(network_name)
    print "step 3: write weights json file"
    net_name = raw_input("       Input the network name:   ")
    time_now = datetime.now().date().strftime('%Y%m%d')
    with open("result_"+time_now+"_"+net_name+".txt",'a+') as file:
        file.write(net_name+"=")
        file.write(jsons)
