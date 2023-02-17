"""

"""
from utils.threading import Threading


class GFF:

    @staticmethod
    def read_gff_files(self, gff_file, genome_name, gff_tag_name, outfile, fa_dict):
        '''
        outfile is combine them into one gff file
        elicit from fasta and gff
        used for mcscanx
        '''
        out_obj=open(outfile, 'w')  
        for name in genome_names:
            #read gene position
            in_obj=open(gff_file, 'r')
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
                        if tag_name == gff_tag_name and ID in fa_dict.keys():
                            if fa_dict[ID]['gff'] is None:#unique line
                                out=[name+'_'+items[0], ID, items[3],items[4]]
                                fa_dict[ID]['gff']=out
                                out_obj.write("{}\n".format('\t'.join(out)))
                                break
            in_obj.close()
                    

        out_obj.close()
        return fa_dict        

    @staticmethod
    def run_gffcompare(self, dir_results, dir_poinfish, genome_gtf_file):
        '''
        compare gff fils
        '''
        #  pinfish/polished_transcripts_collapsed.gff -o gff_compare
        exe="gffcompare -R -M -C -K"
        outdir=ab.basic().format_dir(args.dir_results+'gffcompare')+'gffcompare'
        gff_col = dir_pinfish+'polished_transcripts_collapsed.gff'
        command = "{} -r {} -o {} {}".format(exe, genome_gtf_file, outdir, gff_col)
        #print(command)
        Threading.run_tool(command)