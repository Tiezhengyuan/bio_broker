

class GFF:
    def __init__(self, gff_file):
        self.gff_file = gff_file

    def read_gff_files(self, outfile, fa_dict):
        '''
        outfile is combine them into one gff file
        elicit from fasta and gff
        used for mcscanx
        '''
        out_obj=open(outfile, 'w')  
        for name in self.args.genome_names:
            #read gene position
            in_obj=open(self.gff_file, 'r')
            for line in in_obj:
                line = line.rstrip()
                items=line.split('\t')
                if len(items)==9:#remove comments line
                    annot=re.split(';| ; ', items[8]) #column #9
                    for one in annot:
                        #tage could be geneID or Accession
                        start=re.search('=| ', one).start()
                        tag_name,tag=one[:start], one[(start+1):]
                        ID=name+'_'+tag
                        #print('##{}##{}##{}##'.format(one, tag_name, tag))
                        if tag_name == self.args.gff_tag_name and ID in fa_dict.keys():
                            if fa_dict[ID]['gff'] is None:#unique line
                                out=[name+'_'+items[0], ID, items[3],items[4]]
                                fa_dict[ID]['gff']=out
                                out_obj.write("{}\n".format('\t'.join(out)))
                                break
            in_obj.close()
                    

        out_obj.close()
        return fa_dict        
